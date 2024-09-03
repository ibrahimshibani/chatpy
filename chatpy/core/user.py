class User:
    def __init__(self, user_id, name, password, role):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.status = 'offline'
        self.role = role

    def set_status(self, status):
        if status in ['online', 'offline']:
            self.status = status
        else:
            raise ValueError("Invalid status")

    def is_online(self):
        return self.status == 'online'

    def verify_password(self, password):
        return self.password == password
    
    def __repr__(self):
        return f'{self.name}'