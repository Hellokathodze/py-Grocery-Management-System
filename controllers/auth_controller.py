class AuthController:

    def __init__(self, auth_service):
        self.auth_service = auth_service

    def login(self):

        print("\n===== LOGIN =====")

        username = input("Username: ")
        password = input("Password: ")

        user = self.auth_service.login(username, password)

        if user:
            print("Login successful!")
            return user
        else:
            print("Invalid credentials")
            return None