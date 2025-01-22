import psycopg2
from connection import db_connection, db_params
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='db/.env')


class DataBaseInsertion:
    def __init__(self, connection):
        """
        Initialize with a database connection.
        """
        self.connection = connection

    def insert_data(self, query: str, values: tuple, table_name: str):
        """
        Generic method to insert data into a table.
        :param query: SQL insert query.
        :param values: Tuple of values to insert.
        :param table_name: Name of the table to insert data into.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Data successfully inserted into '{table_name}'!")
        except psycopg2.Error as err:
            self.connection.rollback()
            print(f"Error inserting data into '{table_name}': {err}")
        finally:
            if cursor:
                cursor.close()
            self.connection.autocommit = True


class FlightDataInserter(DataBaseInsertion):
    def insert_to_flight(self, flight_data: tuple):
        """
        Insert a flight record into the flight table.
        :param flight_data: Tuple containing flight data.
        """
        _table_name = "flight"
        query = """
            INSERT INTO flight (
                fk_departure_airport_id,
                fk_arrival_airport_id,
                departure_date,
                arrival_date,
                ticket_price,
                currency_code,
                flight_number,
                price_updated
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.insert_data(query, flight_data, _table_name)


class DepartureDataInserter(DataBaseInsertion):
    def insert_to_departure_airport(self, airport_data: tuple):
        _table_name = "departure_airport"
        query = """
            INSERT INTO departure_airport (
                depart_country_name,
                depart_iata_code,
                depart_airport_name,
                fk_city_depart_id
            ) VALUES (%s, %s, %s, %s)
        """
        self.insert_data(query, airport_data, _table_name)


class ArrivalDataInserter(DataBaseInsertion):
    def insert_to_arrival_airport(self, airport_data: tuple):
        _table_name = "arrival_airport"
        _query = """
            INSERT INTO arrival_airport (
                arriv_country_name,
                arriv_iata_code,
                arriv_airport_name,
                fk_city_arrival_id
            ) VALUES (%s, %s, %s, %s)
        """
        self.insert_data(_query, airport_data, _table_name)


class PricesHistoryDataInserter(DataBaseInsertion):
    def insert_to_prices_history(self, airport_data: tuple):
        _table_name = 'ticket_prices_history'
        _query = \
            """
                INSERT INTO ticket_prices_history (
                    fk_flight_id,
                    price,
                    currency_code,
                    price_added_date
                ) VALUES (%s, %s, %s, %s)
            """

        self.insert_data(_query, airport_data, _table_name)



if "__main__" == __name__:
    connection = db_connection(db_params)
    airport_inserter = ArrivalDataInserter(connection)
    pass
