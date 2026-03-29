class AuthService:

    def __init__(self, db):
        self.users = db["users"]

    def create_default_users(self):

        if self.users.count_documents({"username": "admin"}) == 0:
            self.users.insert_one({
                "username": "admin",
                "password": "admin123",
                "role": "admin"
            })

        if self.users.count_documents({"username": "cashier"}) == 0:
            self.users.insert_one({
                "username": "cashier",
                "password": "cash123",
                "role": "cashier"
            })

    def login(self, username, password):

        user = self.users.find_one({
            "username": username,
            "password": password
        })

        return user