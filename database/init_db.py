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
                            "stock_quantity"
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

                            "stock_quantity": {
                                "bsonType": "int"
                            },

                            "reorder_level": {
                                "bsonType": "int"
                            },

                            "expiry_date": {
                                "bsonType": "string",
                                "description": "Product expiry date in YYYY-MM-DD format"
                            },

                            "created_at": {
                                "bsonType": "string"
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
                            "price_per_unit",
                            "total_price",
                            "sale_date"
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

                            "price_per_unit": {
                                "bsonType": ["double", "int"]
                            },

                            "total_price": {
                                "bsonType": ["double", "int"]
                            },

                            "sale_date": {
                                "bsonType": "string"
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
                                "bsonType": "string"
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
                                "bsonType": "string"
                            }
                        }
                    }
                }
            )

        # USERS COLLECTION (FOR LOGIN SYSTEM)
        if "users" not in self.db.list_collection_names():
            self.db.create_collection("users")

        print("Database initialized successfully!")