class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }


# 🔥 THIS IS YOUR AUTH SERVICE
class UserModel:

    def __init__(self):
        # Dummy users (later replace with DB)
        self.users = [
            User("admin", "admin", "admin"),
            User("user", "1234", "staff")
        ]

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user   # return full user object
        return None