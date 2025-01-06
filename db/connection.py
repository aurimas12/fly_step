import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print("Prisijungimas prie DB sėkmingas.")
        return connection
    except psycopg2.Error as e:
        print(f"Prisijungimo klaida: {e}")
        return None
