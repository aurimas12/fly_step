import psycopg2
from db.connection import db_connection, db_params
#from connection import db_connection, db_params
from dotenv import load_dotenv
from constants import LOAD_DOTENV_PATH
import os

load_dotenv(dotenv_path=LOAD_DOTENV_PATH)


class DbBaseInitializer:
    def __init__(self, connection):
        self.connection = connection

    def table_exists(self, table_name):
        """
        Checks if a table exists in the database.
        :param table_name: Name of the table to check
        :return: True if the table exists, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = %s
                );
            """
            cursor.execute(query, (table_name,))
            exists = cursor.fetchone()[0]
            return exists
        except psycopg2.Error as err:
            print(f"Error checking if table in db '{table_name}' exists:", err)
            return False
        finally:
            if cursor:
                cursor.close()

    def create_table(self, query, table_name):
        """
        Executes the SQL query to create a table.
        :param query: SQL query to create the table
        :param table_name: Name of the table
        """
        cursor  = None
        try:
            if self.table_exists(table_name):
                print(f"Table '{table_name}' already exists!")
                return

            self.connection.autocommit = False
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully!")
        except psycopg2.Error as err:
            print(f"Error creating table '{table_name}':", err)
            self.connection.rollback()
            print(f"Transaction rolled back for table '{table_name}'.")
        finally:
            if cursor is not None:
                cursor.close()

    def query_existing_tables(self):
        """
        Retrieves the list of existing table names in the connected database.
        :return: List of table names in the public schema.
        """
        try:
            cursor = self.connection.cursor()
            database_name = os.getenv('DB_NAME')
            query = f"""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_catalog = '{database_name}'
                AND table_schema = 'public'
            """
            cursor.execute(query)
            existing_tables = [row[0] for row in cursor.fetchall()]
            return existing_tables
        except psycopg2.Error as err:
            print(f"Error querying existing tables: {err}")
            return []
        finally:
            if cursor:
                cursor.close()


class FlightTable(DbBaseInitializer):
    def query_create_table(self):
        _table_name = 'flight'
        _flight_table_query = """
            CREATE TABLE IF NOT EXISTS flight
            (
                flight_id SERIAL NOT NULL,
                fk_route_id INT NOT NULL,
                fk_depart_airport_id INT NOT NULL,
                fk_arriv_airport_id INT NOT NULL,
                departure_date VARCHAR(20) NOT NULL,
                arrival_date VARCHAR(20) NOT NULL,
                ticket_price FLOAT NOT NULL,
                flight_number VARCHAR(10) NOT NULL,
                price_updated_date BIGINT NOT NULL,

                PRIMARY KEY (flight_id),
                CONSTRAINT fk_route
                    FOREIGN KEY (fk_route_id)
                    REFERENCES route(route_id),
                CONSTRAINT fk_depart_airport
                    FOREIGN KEY (fk_depart_airport_id)
                    REFERENCES departure_airport(depart_airport_id),
                CONSTRAINT fk_arriv_airport
                    FOREIGN KEY (fk_arriv_airport_id)
                    REFERENCES arrival_airport(arriv_airport_id)
            );
        """
        self.create_table(_flight_table_query, _table_name)


class PricesHistoryTable(DbBaseInitializer):
    def query_create_table(self):
        _table_name = 'ticket_prices_history'
        _prices_table_query = """
            CREATE TABLE IF NOT EXISTS ticket_prices_history
            (
                ticket_id SERIAL NOT NULL,
                fk_flight_id INT NOT NULL,
                price FLOAT NOT NULL,
                currency_code CHAR(3) NOT NULL,
                price_added_date BIGINT NOT NULL,

                PRIMARY KEY (ticket_id),
                CONSTRAINT fk_flight
                    FOREIGN KEY (fk_flight_id)
                    REFERENCES flight(flight_id)
            );
        """
        self.create_table(_prices_table_query, _table_name)


class RouteTable(DbBaseInitializer):
    def query_create_table(self):
        _table_name = 'route'
        _route_table_query = """
            CREATE TABLE IF NOT EXISTS route (
                route_id SERIAL NOT NULL,
                fk_depart_airport_id INT NOT NULL,
                fk_arriv_airport_id INT NOT NULL,
                flight_number VARCHAR(20) NOT NULL,

                PRIMARY KEY (route_id),
                CONSTRAINT fk_departure_airport
                    FOREIGN KEY (fk_depart_airport_id)
                    REFERENCES departure_airport(depart_airport_id),
                CONSTRAINT fk_arriv_airport
                    FOREIGN KEY (fk_arriv_airport_id)
                    REFERENCES arrival_airport(arriv_airport_id)
            );
        """
        self.create_table(_route_table_query, _table_name)


class DepartureAirportTable(DbBaseInitializer):
    def query_create_table(self):
        _table_name = 'departure_airport'
        _departure_airport_table_query = """
            CREATE TABLE IF NOT EXISTS departure_airport
            (
                depart_airport_id SERIAL NOT NULL,
                depart_country_name VARCHAR(60) NOT NULL,
                depart_iata_code CHAR(5) NOT NULL,
                depart_airport_name VARCHAR(60) NOT NULL,
                fk_city_id INT NOT NULL,

                PRIMARY KEY (depart_airport_id),
                CONSTRAINT fk_city
                    FOREIGN KEY (fk_city_id)
                    REFERENCES city (city_id)
            );
        """
        self.create_table(_departure_airport_table_query, _table_name)

class CityTable(DbBaseInitializer):
    def query_create_table(self):
        _table_name = 'city'
        _city_departure_table_query = """
            CREATE TABLE IF NOT EXISTS city
            (
                city_id SERIAL NOT NULL,
                city_name VARCHAR(60) NOT NULL,
                code VARCHAR(60) NOT NULL,
                country_code VARCHAR(10) NOT NULL,

                PRIMARY KEY (city_id)
            );
        """
        self.create_table(_city_departure_table_query, _table_name)


class ArrivalAirportTable(DbBaseInitializer):
    def query_create_table(self):
        _table_name = 'arrival_airport'
        _arrival_airport_table_query = """
            CREATE TABLE IF NOT EXISTS arrival_airport
            (
                arriv_airport_id SERIAL NOT NULL,
                arriv_country_name VARCHAR(60) NOT NULL,
                arriv_iata_code VARCHAR(5) NOT NULL,
                arriv_airport_name VARCHAR(60) NOT NULL,
                fk_city_id INT NOT NULL,

                PRIMARY KEY (arriv_airport_id),
                CONSTRAINT fk_city
                    FOREIGN KEY (fk_city_id)
                    REFERENCES city (city_id)
            );
        """
        self.create_table(_arrival_airport_table_query, _table_name)


def create_all_tables_main():
    connection = db_connection(db_params)

    city_table = CityTable(connection)
    departure_airport_table = DepartureAirportTable(connection)
    arrival_airport_table = ArrivalAirportTable(connection)
    route_table = RouteTable(connection)
    flight_table = FlightTable(connection)
    prices_history_table = PricesHistoryTable(connection)

    for table in (city_table, departure_airport_table, arrival_airport_table,
                route_table, flight_table, prices_history_table):
        table.query_create_table()
    connection.close()


if __name__ == '__main__':
    create_all_tables_main()
