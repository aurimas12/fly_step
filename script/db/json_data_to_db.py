import psycopg2
from connection import db_connection, db_params
from dotenv import load_dotenv
#import os
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from flight_data_process import FlightData
from constants import VNO_BCN_DATA_JSON_PATH
from  file import read_load_json_file


load_dotenv(dotenv_path='script/db/.env')


json_data = {
        "departureAirport": {
            "countryName": "Lithuania",
            "iataCode": "KUN",
            "name": "Kaunas",
            "city": {
                "name": "Kaunas",
                "code": "KAUNAS",
                "countryCode": "lt"
            }
        },
        "arrivalAirport": {
            "countryName": "Spain",
            "iataCode": "ALC",
            "name": "Alicante",
            "city": {
                "name": "Alicante",
                "code": "ALICANTE",
                "countryCode": "es"
            }
        },
        "departureDate": "2025-07-14T16:20:00",
        "arrivalDate": "2025-07-14T19:20:00",
        "price": {
            "values": [
                {
                    "timestamp": 1736970400,
                    "value": 70.99
                },
            ],
            "currencyCode": "EUR"
        },
        "flightNumber": "FR6429",
        "priceUpdated": 1736962797000
 }


class DataBaseInsertion:
    def __init__(self, connection):
        """
        Initialize a database connection.
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

    def query_existing_tables(self):
        """
        Retrieves the list of existing table names in the
        connected database's public schema.
        :return: List of table names.
        """
        try:
            cursor = self.connection.cursor()
            db_name = self.connection.get_dsn_parameters().get('dbname')
            query = f"""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_catalog = '{db_name}'
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

    def get_connection_parameters(self):
        """
        Retrieve and return the connection's DSN parameters.
        """
        try:
            dsn_params = self.connection.get_dsn_parameters()
            print("DSN Parameters:")
            return dsn_params
        except psycopg2.Error as err:
            print(f"Error retrieving DSN parameters: {err}")
            return None


#class FlightDataInserter(DataBaseInsertion):
#    def insert_to_flight(self, flight_data: FlightData):
#        _flight_data_tuple = self._extract_flight_data(flight_data)
#        _table_name = "flight"
#        _query = \
#            """
#                INSERT INTO flight (
#                    fk_departure_airport_id,
#                    fk_arrival_airport_id,
#                    departure_date,
#                    arrival_date,
#                    ticket_price,
#                    currency_code,
#                    flight_number,
#                    price_updated
#                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#            """
#        self.insert_data(_query, _flight_data_tuple, _table_name)

#    def _extract_flight_data(self, flight_data: FlightData):
#        flight_data_tuple = (
#            flight_data.get_departure_country_name(),
#            flight_data.get_departure_airport_iata(),
#            flight_data.get_departure_airport_name(),
#        )
#        return flight_data_tuple


#class DepartureDataInserter(DataBaseInsertion):
#    def insert_to_departure_airport(self, flight_data: FlightData):
#        _flight_data_tuple = self._extract_departure_data(flight_data)
#        _table_name = "departure_airport"
#        query = \
#        """
#                INSERT INTO departure_airport (
#                    depart_country_name,
#                    depart_iata_code,
#                    depart_airport_name,
#                    fk_city_depart_id
#                ) VALUES (%s, %s, %s, %s)
#            """
#        self.insert_data(query, _flight_data_tuple, _table_name)

#    def _extract_departure_data(self, flight_data: FlightData):
#        flight_data_tuple = (
#            flight_data.get_departure_country_name(),
#            flight_data.get_departure_airport_iata(),
#            flight_data.get_departure_airport_name(),
#        )
#        return flight_data_tuple


#class ArrivalDataInserter(DataBaseInsertion):
#    def insert_to_arrival_airport(self, flight_data: FlightData):
#        _flight_data_tuple = self._extract_arrival_data(flight_data)
#        _table_name = "arrival_airport"
#        _query = \
#            """
#                INSERT INTO arrival_airport (
#                    arriv_country_name,
#                    arriv_iata_code,
#                    arriv_airport_name,
#                    fk_city_arrival_id
#                ) VALUES (%s, %s, %s, %s)
#            """
#        self.insert_data(_query, _flight_data_tuple, _table_name)

#    def _extract_arrival_data(self, flight_data: FlightData):
#        flight_data_tuple = (
#            flight_data.get_arrival_country_name(),
#            flight_data.get_arrival_airport_iata(),
#            flight_data.get_arrival_airport_name(),
#        )
#        return flight_data_tuple


class PricesHistoryDataInserter(DataBaseInsertion):
    def insert_to_prices_history(self, flight_data: FlightData):
        _flight_data_tuple = self._extract_rices_history_data(flight_data)
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

        self.insert_data(_query, _flight_data_tuple, _table_name)

    def _extract_rices_history_data(self, flight_data: FlightData):
        flight_data_tuple = (
            flight_data.get_latest_price(),
            flight_data.get_currency_code,
            flight_data.get_latest_prices_timestamp(),
        )
        return flight_data_tuple


class RouteTableDataInserter(DataBaseInsertion):
    def insert_to_route(self, flight_data: FlightData):
        _flight_data_tuple = self._extract_route_data(flight_data)
        _table_name = 'route'
        _query = \
            """
                INSERT INTO route (
                    fk_departure_airport_id,
                    fk_arrival_airport_id,
                    flight_number,
                ) VALUES (%s, %s, %s)
             """
        self.insert_data(_query, _flight_data_tuple, _table_name)

    def _extract_route_data(self, flight_data: FlightData):
        flight_data_tuple = (
            flight_data.get_flight_number(),
        )
        return flight_data_tuple


class CityDataInserter(DataBaseInsertion):
    def insert_to_city(self, flight_data: FlightData):
        _flight_data_tuple = self._extract_city_depart_data(flight_data)
        _table_name = 'city'
        _query = \
            """
                INSERT INTO city (
                    city_name,
                    code,
                    country_code,
                ) VALUES (%s, %s, %s)
            """
        self.insert_data(_query, _flight_data_tuple, _table_name)

    def _extract_city_depart_data(self, flight_data: FlightData):
        flight_data_tuple = (
            flight_data.get_departure_city_name(),
            flight_data.get_departure_city_code(),
            flight_data.get_departure_country_code(),
        )
        return flight_data_tuple

    def _extract_city_arriv_data(self, flight_data: FlightData):
        flight_data_tuple = (
            flight_data.get_arrival_city_name(),
            flight_data.get_arrival_city_code(),
            flight_data.get_arrival_country_code(),
        )
        return flight_data_tuple

if "__main__" == __name__:
    flight_data = FlightData(json_data)
    print(flight_data)
    print(flight_data.get_prices_list())
    print(flight_data.get_prices_timestamp_list())
    print(flight_data.get_latest_price())
    print(flight_data.get_latest_prices_timestamp())

    #connection = db_connection(db_params)
    #c = DataBaseInsertion(connection)
    #print(c.query_existing_tables())
    #print(c.get_connection_parameters())

    #json_data = read_load_json_file(VNO_BCN_DATA_JSON_PATH)
    #print(json_data[1])
#    #airport_inserter = ArrivalDataInserter(connection)
#    pass
