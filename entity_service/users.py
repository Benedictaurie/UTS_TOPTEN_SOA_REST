import hashlib

class User:
    def __init__(self, users_id, name, email, password, phone_number):
        self.id = users_id
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number

    def set_password(self, plain_password):
        self.password = hashlib.md5(plain_password.encode()).hexdigest()

    def to_dict(self):
        return {
            "users_id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number
        }

    def __repr__(self):
        return f"<User {self.id}: {self.email}>"