import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Default user in XAMPP
        password="",  # Empty password in XAMPP
        database="telegram_store"
    )

def get_product_details(product_code):
    db = connect_db()
    cursor = db.cursor()
    
    query = "SELECT name, price, available_stock, colors FROM products WHERE code = %s"
    cursor.execute(query, (product_code,))
    product = cursor.fetchone()

    db.close()

    return product


# Test Connection
if __name__ == "__main__":
    test_code = "P0001"
    product = get_product_details(test_code)
    if product:
        print(f"Product Found: {product}")
    else:
        print(f"Product Not Found.")

