from db.connection import get_connection
from utils.helpers import handle_db_error, get_last_inserted_id, format_user, execute_query_with_params
import psycopg2

def main():
    connection = get_connection()
    if connection is None:
        print("Nepavyko prisijungti prie duomenų bazės.")
        return

    try:
        cursor = connection.cursor()

        # Pvz., įterpiame vartotoją
        insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        execute_query_with_params(cursor, insert_query, ("Petras", "petras@example.com"))

        # Pasiimame paskutinį įrašytą ID
        last_id = get_last_inserted_id(cursor)
        print(f"Paskutinis įrašytas ID: {last_id}")

        connection.commit()

    except psycopg2.Error as e:
        handle_db_error(e)
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    main()
