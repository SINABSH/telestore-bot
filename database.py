import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Default user in XAMPP
        password=DB_PASSWORD,
        database=DB_NAME
    )

def save_order(product_code, quantity, customer_name, address, phone):
    conn = connect_db()
    cursor = conn.cursor()

