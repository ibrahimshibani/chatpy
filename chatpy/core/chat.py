from chatpy.core.message import Message
from datetime import datetime

class Chat:
    def __init__(self, customer, agent):
        self.customer = customer
        self.agent = agent
        self.messages = []
        self.start_time = datetime.now()
        self.session_id = self.generate_sess_id()

    # as we use this for auth, should be more secure
    def generate_sess_id(self):
        return f"{self.customer.user_id}_{self.agent.user_id}_{int(datetime.now().timestamp())}"

    def send_message(self, sender, receiver, content):
        message = Message(len(self.messages) + 1, sender, receiver, content)
        self.messages.append(str(message))
        return message

    def get_session_messages(self):
        return self.messages

    def __repr__(self):
        return f'ChatObject{self.messages}'