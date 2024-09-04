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
def load_users():
    """
    Load users from the user database and create User objects.

    This function iterates over the values in the user_db dictionary and creates User objects for each user. The User objects are then stored in the users dictionary using the user_id as the key.

    Parameters:
    None

    Returns:
    None
    """
    for user_data in user_db.values():
        user = User(
            user_id=user_data['user_id'],
            name=user_data['name'],
            password=user_data['password'],
            role=user_data['role']
        )
        users[user.user_id] = user

def update_db():
    """
    Updates the user database by writing the contents of `user_db` to a JSON file.

    Parameters:
        None

    Returns:
        None
    """
    with open('data/user_db.json', 'w') as f:
        json.dump(user_db, f)

load_users()


@app.route('/login', methods=['POST'])
def login():
    """
    API endpoint for user login.
    Parameters:
    - username (str): The username of the user.
    - password (str): The password of the user.
    Returns:
    - JSON response: A JSON response containing the following fields:
        - message (str): A message indicating whether the login was successful.
        - user_id (str): The ID of the logged-in user.
        - role (str): The role of the logged-in user.
        If the login is successful, the response status code will be 200.
        If the username or password is invalid, the response status code will be 401.
    """    
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
    """
    Starts a new chat session between a customer and an agent.
    Endpoint: /start_session
    Method: POST
    Parameters:
    - customer_id (str): The ID of the customer.
    - agent_id (str): The ID of the agent.
    Returns:
    - If the customer and agent IDs are valid and their roles are 'customer' and 'agent' respectively, a JSON response with the following fields:
        - success (str): A success message indicating that the session has started.
        - session_id (str): The ID of the newly created chat session.
        - status code 200.
    - If the customer or agent ID is invalid or their roles are not 'customer' and 'agent' respectively, a JSON response with the following field:
        - error (str): An error message indicating that the customer or agent ID is invalid.
        - status code 400.
    """
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
    """
    API endpoint for sending a message.
    Parameters:
    - session_id (str): The session ID for the chat instance.
    - sender_id (str): The ID of the sender.
    - receiver_id (str): The ID of the receiver.
    - content (str): The content of the message.
    Returns:
    - JSON response:
        - message_id (str): The ID of the sent message.
        - sender (str): The name of the sender.
        - receiver (str): The name of the receiver.
        - content (str): The content of the message.
        - timestamp (str): The timestamp of the message.
    Raises:
    - ValueError: If there is an error sending the message.
    """    
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
    """
    Get messages for a given session ID.
    Parameters:
    - session_id (str): The ID of the session.
    Returns:
    - response (str): The chat history for the session.
    - status_code (int): The HTTP status code of the response.
    Raises:
    - 404 (Not Found): If the session ID is not found.
    """
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
    """
    API endpoint to check if any agent is online.

    Returns:
        - If an online agent is found:
            - agent_id (int): The ID of the online agent.
            - status (str): The status of the agent, which is "online".
            - agent_name (str): The name of the online agent.
        - If no online agents are found:
            - message (str): A message indicating that no agents are online.
    """    
    for user_id, user in user_db.items():
        if user['role'] == 'agent' and user['status'] == 'online':
            return jsonify({"agent_id": user_id, "status": "online", "agent_name": user["name"]}), 200
    return jsonify({"message": "No agents are online"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)
