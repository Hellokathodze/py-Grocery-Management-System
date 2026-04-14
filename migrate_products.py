"""
ONE-TIME MIGRATION SCRIPT
=========================
Run this ONCE to add missing 'expiry_date' and 'reorder_level'
fields to existing products that don't have them.

Usage:
    python migrate_products.py

After running, verify in MongoDB Compass that all products
now have both fields. Then you can delete this script.
"""

from pymongo import MongoClient
from datetime import datetime, timedelta


def migrate():

    # ====== UPDATE THIS IF YOUR CONNECTION STRING IS DIFFERENT ======
    client = MongoClient("mongodb://localhost:27017/")
    db = client["grocery_management"]
    products = db["products"]

    # Count products missing each field
    missing_expiry = products.count_documents({
        "$or": [
            {"expiry_date": {"$exists": False}},
            {"expiry_date": None},
            {"expiry_date": ""}
        ]
    })

    missing_reorder = products.count_documents({
        "$or": [
            {"reorder_level": {"$exists": False}},
            {"reorder_level": None}
        ]
    })

    print(f"\nProducts missing expiry_date:  {missing_expiry}")
    print(f"Products missing reorder_level: {missing_reorder}")

    if missing_expiry == 0 and missing_reorder == 0:
        print("\n✅ All products already have both fields. Nothing to do!")
        client.close()
        return

    # ====== DEFAULT VALUES ======
    # Default expiry: 6 months from today
    default_expiry = (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d")

    # Default reorder level: 10
    default_reorder = 10

    print(f"\nDefault expiry_date:  {default_expiry}")
    print(f"Default reorder_level: {default_reorder}")
    print()

    # ====== ADD MISSING expiry_date ======
    if missing_expiry > 0:
        result = products.update_many(
            {
                "$or": [
                    {"expiry_date": {"$exists": False}},
                    {"expiry_date": None},
                    {"expiry_date": ""}
                ]
            },
            {
                "$set": {"expiry_date": default_expiry}
            }
        )
        print(f"✅ Added expiry_date to {result.modified_count} product(s)")

    # ====== ADD MISSING reorder_level ======
    if missing_reorder > 0:
        result = products.update_many(
            {
                "$or": [
                    {"reorder_level": {"$exists": False}},
                    {"reorder_level": None}
                ]
            },
            {
                "$set": {"reorder_level": default_reorder}
            }
        )
        print(f"✅ Added reorder_level to {result.modified_count} product(s)")

    # ====== VERIFY ======
    print("\n--- Verification ---")
    all_products = list(products.find({}, {"_id": 0, "product_id": 1, "product_name": 1, "expiry_date": 1, "reorder_level": 1}))

    for p in all_products:
        pid = p.get("product_id", "?")
        name = p.get("product_name", "?")
        expiry = p.get("expiry_date", "MISSING")
        reorder = p.get("reorder_level", "MISSING")
        print(f"  {pid} - {name:<25} expiry: {expiry}   reorder: {reorder}")

    print(f"\n✅ Migration complete! {len(all_products)} products verified.")

    client.close()


if __name__ == "__main__":
    migrate()