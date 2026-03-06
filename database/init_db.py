class DatabaseInitializer:

    def __init__(self, db):
        self.db = db


    def initialize_collections(self):

        # PRODUCTS COLLECTION
        if "products" not in self.db.list_collection_names():

            self.db.create_collection(
                "products",
                validator={
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": [
                            "product_id",
                            "product_name",
                            "category",
                            "price",
                            "stock"
                        ],
                        "properties": {

                            "product_id": {
                                "bsonType": "string"
                            },

                            "product_name": {
                                "bsonType": "string"
                            },

                            "category": {
                                "bsonType": "string"
                            },

                            "price": {
                                "bsonType": ["double", "int"]
                            },

                            "stock": {
                                "bsonType": "int"
                            }

                        }
                    }
                }
            )

        # SALES COLLECTION
        if "sales" not in self.db.list_collection_names():

            self.db.create_collection(
                "sales",
                validator={
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": [
                            "product_id",
                            "product_name",
                            "quantity",
                            "price",
                            "total_price",
                            "date"
                        ],
                        "properties": {

                            "product_id": {
                                "bsonType": "string"
                            },

                            "product_name": {
                                "bsonType": "string"
                            },

                            "quantity": {
                                "bsonType": "int"
                            },

                            "price": {
                                "bsonType": ["double", "int"]
                            },

                            "total_price": {
                                "bsonType": ["double", "int"]
                            },

                            "date": {
                                "bsonType": "date"
                            },

                            "day_of_week": {
                                "bsonType": "string"
                            },

                            "month": {
                                "bsonType": "int"
                            },

                            "season": {
                                "bsonType": "string"
                            }

                        }
                    }
                }
            )

        # PURCHASES COLLECTION
        if "purchases" not in self.db.list_collection_names():

            self.db.create_collection(
                "purchases",
                validator={
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": [
                            "product_id",
                            "product_name",
                            "quantity",
                            "price",
                            "date"
                        ],
                        "properties": {

                            "product_id": {
                                "bsonType": "string"
                            },

                            "product_name": {
                                "bsonType": "string"
                            },

                            "quantity": {
                                "bsonType": "int"
                            },

                            "price": {
                                "bsonType": ["double", "int"]
                            },

                            "date": {
                                "bsonType": "date"
                            }

                        }
                    }
                }
            )

        # STOCK MOVEMENTS COLLECTION
        if "stock_movements" not in self.db.list_collection_names():

            self.db.create_collection(
                "stock_movements",
                validator={
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": [
                            "product_id",
                            "movement_type",
                            "quantity",
                            "date"
                        ],
                        "properties": {

                            "product_id": {
                                "bsonType": "string"
                            },

                            "movement_type": {
                                "bsonType": "string"
                            },

                            "quantity": {
                                "bsonType": "int"
                            },

                            "date": {
                                "bsonType": "date"
                            }

                        }
                    }
                }
            )

        print("Database initialized successfully!")