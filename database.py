import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Fetch product details by product code
def get_product_details(product_code):
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT name, price, stock, colors FROM products WHERE product_code = %s"
    cursor.execute(query, (product_code,))
    product = cursor.fetchone()

    cursor.close()
    conn.close()
    return product  # Returns (name, price, stock, colors) or None if not found

# Store a new order in the database
def save_order(product_code, quantity, customer_name, address, phone):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO orders (product_code, quantity, customer_name, address, phone)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (product_code, quantity, customer_name, address, phone))
    conn.commit()
    order_id = cursor.lastrowid  # Get the ID of the new order

    cursor.close()
    conn.close()
    return order_id  # Return the order ID to show the customer
