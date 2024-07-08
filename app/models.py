from datetime import datetime

class User:
    def __init__(self, id, username, password_hash, email, created_at=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
    def from_dict(data):
        return User(
            id=data['id'],
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            created_at=datetime.fromisoformat(data.get('created_at'))
        )