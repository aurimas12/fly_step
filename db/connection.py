import os
import psycopg2
from dotenv import load_dotenv


load_dotenv(dotenv_path='db/.env')

db_params = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def db_connection(db_params):
    try:
        connection = psycopg2.connect(connect_timeout=10, **db_params)
        print(f"Prisijungimas prie '{db_params['database']}' DB sėkmingas.")
        return connection
    except psycopg2.Error as e:
        print(f"Prisijungimo klaida: {e}")
        return None
    except Exception as e:
        print(f"An error connecting to the database: {e}")
        return None
