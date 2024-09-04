from datetime import datetime

class Message:
    def __init__(self, message_id, sender, receiver, content):
        self.message_id = message_id
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]     {self.sender}: {self.content}"

