import psycopg2
from connection import db_connection, db_params
from dotenv import load_dotenv
import os

# TODO: from scripyt to  db

from script.flight_data_process import FlightData
#import script.flight_data_process
#from ..script.flight_data_process import FlightData
#from script.file import read_load_json_file
#from script.constants import vno_bcn_data_json_path

load_dotenv(dotenv_path='db/.env')


##json_data = {
##        "departureAirport": {
##            "countryName": "Lithuania",
##            "iataCode": "KUN",
##            "name": "Kaunas",
##            "city": {
##                "name": "Kaunas",
##                "code": "KAUNAS",
##                "countryCode": "lt"
##            }
##        },
##        "arrivalAirport": {
##            "countryName": "Spain",
##            "iataCode": "ALC",
##            "name": "Alicante",
##            "city": {
##                "name": "Alicante",
##                "code": "ALICANTE",
##                "countryCode": "es"
##            }
##        },
##        "departureDate": "2025-07-14T16:20:00",
##        "arrivalDate": "2025-07-14T19:20:00",
##        "price": {
##            "values": [
##                {
##                    "timestamp": 1736970568,
##                    "value": 83.99
##                }
##            ],
##            "currencyCode": "EUR"
##        },
##        "flightNumber": "FR6429",
##        "priceUpdated": 1736962797000
##    }

#class DataBaseInsertion:
#    def __init__(self, connection):
#        """
#        Initialize with a database connection.
#        """
#        self.connection = connection

#    def insert_data(self, query: str, values: tuple, table_name: str):
#        """
#        Generic method to insert data into a table.
#        :param query: SQL insert query.
#        :param values: Tuple of values to insert.
#        :param table_name: Name of the table to insert data into.
#        """
#        try:
#            cursor = self.connection.cursor()
#            cursor.execute(query, values)
#            self.connection.commit()
#            print(f"Data successfully inserted into '{table_name}'!")
#        except psycopg2.Error as err:
#            self.connection.rollback()
#            print(f"Error inserting data into '{table_name}': {err}")
#        finally:
#            if cursor:
#                cursor.close()
#            self.connection.autocommit = True


#class FlightDataInserter(DataBaseInsertion):
#    def insert_to_flight(self, flight_data: tuple):
#        """
#        Insert a flight record into the flight table.
#        :param flight_data: Tuple containing flight data.
#        """
#        _table_name = "flight"
#        query = \
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
#        self.insert_data(query, flight_data, _table_name)


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
#    def insert_to_arrival_airport(self, airport_data: tuple):
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
#        self.insert_data(_query, airport_data, _table_name)


#class PricesHistoryDataInserter(DataBaseInsertion):
#    def insert_to_prices_history(self, airport_data: tuple):
#        _table_name = 'ticket_prices_history'
#        _query = \
#            """
#                INSERT INTO ticket_prices_history (
#                    fk_flight_id,
#                    price,
#                    currency_code,
#                    price_added_date
#                ) VALUES (%s, %s, %s, %s)
#            """

#        self.insert_data(_query, airport_data, _table_name)


#class RouteTableDataInserter(DataBaseInsertion):
#    def insert_to_route(self, airport_data: tuple):
#        _table_name = 'route'
#        _query = \
#            """
#                INSERT INTO route (
#                    fk_departure_airport_id,
#                    fk_arrival_airport_id,
#                    flight_number,
#                ) VALUES (%s, %s, %s)
#             """
#        self.insert_data(_query, airport_data, _table_name)


#class CityDataInserter(DataBaseInsertion):
#    def insert_to_city(self, airport_data: tuple):
#        _table_name = 'city'
#        _query = \
#            """
#                CREATE TABLE IF NOT EXISTS city (
#                    city_name,
#                    code,
#                    country_code,
#                ) VALUES (%s, %s, %s)
#            """
#        self.insert_data(_query, airport_data, _table_name)


if "__main__" == __name__:
    connection = db_connection(db_params)
#    json_data = read_load_json_file(vno_bcn_data_json_path)
#    print(json_data[1])
#    #airport_inserter = ArrivalDataInserter(connection)
#    pass
