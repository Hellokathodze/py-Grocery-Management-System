from pymongo import MongoClient


class DatabaseConnection:

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["grocery_management"]

    def get_database(self):
        return self.db