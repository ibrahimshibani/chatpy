# ChatPY
 Simple chat application built for demo / learning purposes. It allows Customer of a company to chat with agents. The streamlit interface is designed to work only for customers, the assumption here is that agents would have their console.


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ibrahimshibani/chatpy.git
    cd chatpy
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    python -m pip install -r requirements.txt
    ```

## Usage

1. Start the Flask server (by default it will run in default mode in port 8000):
    ```sh
    python main.py
    ```

2. Open another terminal and start the Streamlit app:
    ```sh
    streamlit run st_app.py
    ```

3. Open your web browser and navigate to `http://localhost:8501` to access the Streamlit app.

## Emulate Agent Activity

To emulate agent activity, you can use the following `curl` commands to log in as an agent and send a message.

### Login as Agent

```sh
curl -X POST http://localhost:8000/login \
     -H "Content-Type: application/json" \
     -d '{
           "username": "agent_username",
           "password": "agent_password"
         }'
```
Replace agent_username and agent_password with the actual credentials of the agent.

### Send Message as Agent
After logging in, you can send a message in a chat session using the following command:

Replace your_session_id with the actual session ID and agent_username with the agent's username. Customize the message field with the message you want to send.
```sh

curl -X POST http://localhost:8000/send_message \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "your_session_id",
           "sender": "agent_username",
           "message": "Hello, how can I assist you today?"
         }'
```
Replace your_session_id with the actual session ID and agent_username with the agent's username. Customize the message field with the message you want to send.


## API Endpoints

- **POST /login**: User login
- **POST /start_session**: Start a new chat session
- **POST /send_message**: Send a message in a chat session
- **GET /get_messages/<session_id>**: Retrieve messages for a chat session
- **GET /get_free_agent**: Check if any agent is online



## Data

The user database is stored in [`data/user_db.json`] and contains user information such as user ID, name, password, role, and status.

## License

This project is licensed under the MIT License.