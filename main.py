import json
from flask import Flask, request, jsonify, make_response
from chatpy.core.chat import Chat
from chatpy.core.user import User

app = Flask(__name__)
# Load initial state of user db
with open('data/user_db.json', 'r') as f:
    user_db = json.load(f)

users = {}
user_sessions = {}  # active chat sessions by session ID

# helper functions to manipulate user database
# load users from json db as user objects
def load_users():
    for user_data in user_db.values():
        user = User(
            user_id=user_data['user_id'],
            name=user_data['name'],
            password=user_data['password'],
            role=user_data['role']
        )
        users[user.user_id] = user
load_users()
# to be called after manipulating user objects to update json db
def update_db():
    with open('data/user_db.json', 'w') as f:
        json.dump(user_db, f)




@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = next((user for user in user_db.values() if user['name'] == username), None)
    if user and user['password'] == password:
        user['status'] = 'online'
        update_db()
        load_users()

        return jsonify({"message": "Login successful", "user_id": user['user_id'], "role": user["role"]}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/start_session', methods=['POST'])
def start_session():
    data = request.json
    customer_id = data.get('customer_id')
    agent_id = data.get('agent_id')
    load_users()
    customer = users.get(customer_id)
    agent = users.get(agent_id)

    if customer and agent and customer.role == 'customer' and agent.role == 'agent':
        # new chat instance for new session
        chat_instance = Chat(customer, agent)

        user_sessions[chat_instance.session_id] = chat_instance  # multiple sessions per server possible.

        return jsonify({"success": "Session started.", "session_id": chat_instance.session_id}), 200
    else:
        return jsonify({"error": "Invalid customer or agent ID"}), 400

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    session_id = data.get('session_id')

    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')

    sender = users.get(sender_id)
    receiver = users.get(int(receiver_id))
    chat_instance = user_sessions.get(session_id)
    if sender and receiver and chat_instance:
        try:
            message = chat_instance.send_message(sender, receiver, content)

            return jsonify({
                "message_id": message.message_id,
                "sender": sender.name,
                "receiver": receiver.name,
                "content": message.content,
                "timestamp": message.timestamp
            }), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
    else:
        return jsonify({"error": "Invalid sender or receiver ID"}), 400

@app.route('/get_messages/<string:session_id>', methods=['GET'])
def get_messages(session_id):
    chat_instance = user_sessions.get(session_id)    

    if chat_instance:
        messages = chat_instance.get_session_messages()
        chat_history = "\n".join(messages)
        response = make_response(chat_history, 200)
        response.mimetype = "text/plain"
        return response, 200
    else:
        return jsonify({"error": "Session not found"}), 404

@app.route('/get_free_agent', methods=['GET'])
def is_any_agent_online():
    for user_id, user in user_db.items():
        if user['role'] == 'agent' and user['status'] == 'online':
            return jsonify({"agent_id": user_id, "status": "online", "agent_name": user["name"]}), 200
    return jsonify({"message": "No agents are online"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)
