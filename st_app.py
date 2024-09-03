import streamlit as st
import requests
import time

chat_server = "http://127.0.0.1:8000"

if "active_session" not in st.session_state:
    st.session_state["active_session"] = False
if "session_id" not in st.session_state:
    st.session_state["session_id"] = None

def clear_state():
    st.session_state["agent_id"] = None    
    st.session_state["session_id"] = None

st.title("ChatPY")
st.header("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    clear_state()
    login_data = {"username": username, "password": password}
    response = requests.post(f"{chat_server}/login", json=login_data)

    if response.status_code == 200 and response.json()["role"] == "customer":
        st.session_state["user_id"] = response.json()["user_id"]
        st.success("Login successful!")
        st.session_state["active_session"] = True
    else:
        st.error("Login failed. Please check your credentials.")

if st.session_state["active_session"] and st.session_state["session_id"] is None:
    st.header("Start a Chat Session")

    with st.spinner("Assigning you to an agent, please wait..."):
        agent_found = False
        while not agent_found:
            response = requests.get(f"{chat_server}/get_free_agent")
            
            if response.status_code == 200:
                agent_data = response.json()

                st.session_state["agent_id"] = agent_data["agent_id"]
                st.session_state["agent_name"] = agent_data["agent_name"]
                agent_found = True
            else:
                time.sleep(10)
    st.success(f"Assigned to agent: {st.session_state['agent_name']}")

    session_data = {
        "customer_id": st.session_state["user_id"],
        "agent_id": int(st.session_state["agent_id"])
    }
    response = requests.post(f"{chat_server}/start_session", json=session_data)
    
    if response.status_code == 200:
        st.session_state["session_id"] = response.json()["session_id"]
        st.success(f"Session started! Session ID: {st.session_state['session_id']}")
    else:
        st.error("Failed to start session.")

def refresh_chat():
    chat_history = None

    response = requests.get(f"{chat_server}/get_messages/{st.session_state['session_id']}")
    
    if response.status_code == 200:
        messages = response
        chat_history = messages.text
        st.text_area("Chat History", value=chat_history, height=300, disabled=True)
    else:
        st.error("Failed to retrieve messages.")

if st.session_state["session_id"]:
    st.header("Send a Message")
    sender_id = st.session_state["user_id"]
    receiver_id = st.session_state["agent_id"]
    message_content = st.text_area("Message")

    if st.button("Send Message"):
        message_data = {
            "session_id": st.session_state["session_id"],
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "content": message_content
        }
        response = requests.post(f"{chat_server}/send_message", json=message_data)

        if response.status_code == 200:
            st.success("Message sent!")
            refresh_chat()
        else:
            st.error("Failed to send message.")

if st.session_state["session_id"]:

    st.header("Session Messages")

    if st.button("Refresh Messages"):

        refresh_chat()



