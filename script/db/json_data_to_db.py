import psycopg2
from db.connection import db_connection, db_params
from dotenv import load_dotenv
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from count_timer import get_yesterday_timestamp
from flight_data_process import FlightData
from constants import LT_SPAIN_DATA_JSON_PATH, LOAD_DOTENV_PATH
from file import read_load_json_file
from typing import List, Tuple

load_dotenv(dotenv_path=LOAD_DOTENV_PATH)

class DataBaseInsertion:
    def __init__(self, connection):
        """
        Initializes a database connection.
        Args:
            connection: Database connection object.
        """
        self.connection = connection

    def insert_data_to_db(self, query: str, values: tuple, table_name: str) -> bool:
        """
        Inserts data into the specified table.
        Args:
            query (str): SQL INSERT query with placeholders.
            values (tuple): Values to be inserted into the table.
            table_name (str): Name of the table to insert data into.
        Returns:
            bool: True if insertion is successful, False otherwise.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Data successfully inserted into '{table_name}'!")
        except psycopg2.Error as err:
            self.connection.rollback()
            print(f"Error inserting data into '{table_name}': {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def update_data_in_db(self, query: str, values: tuple, table_name: str) -> bool:
        """
        Updates data in the specified table.
        Args:
            query (str): SQL UPDATE query with placeholders.
            values (tuple): Values to update in the table.
            table_name (str): Name of the table being updated.
        Returns:
            bool: True if the update is successful, False otherwise.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Successfully update_data_in_db in '{table_name}'!")
            return True
        except psycopg2.Error as err:
            self.connection.rollback()
            print(f"Error update_data_in_db data in '{table_name}': {err}")
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_data_from_db(self, query: str, values: tuple = ()) -> list:
        """
        Retrieves multiple rows from a database table.
        Args:
            query (str): SQL SELECT query with placeholders.
            values (tuple, optional): Parameters for the query. Defaults to ().
        Returns:
            list: List of fetched records.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                result = cursor.fetchall()
                return result
        except psycopg2.Error as err:
            print(f"Error fetch_data_from_db DataBaseInsertion: {err}")
            return []
        finally:
            if cursor:
                cursor.close()

    def fetch_one_from_db(self, query, values: tuple):
        """
        Retrieves a single record from the database.
        Args:
            query (str): SQL SELECT query with placeholders.
            values (tuple): Parameters for the query.
        Returns:
            Any: The first column of the first row, or None if no results.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result is not None:
                return result[0]
            else:
                return None

        except psycopg2.Error as err:
            print(f"Database error: {err}")
            return None

        finally:
            if cursor:
                cursor.close()

    def insert_data_returning_id(self, query: str, values: tuple, table_name: str):
        """
        Inserts data into a table and returns the primary key ID.
        If the row already exists, fetches the existing ID instead.
        Args:
            query (str): SQL INSERT query with a RETURNING clause.
            values (tuple): Values to insert.
            table_name (str): Name of the table.
         Returns:
            int | None: The primary key ID of the inserted row, or None if insertion failed.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            inserted_id = cursor.fetchone()[0]
            self.connection.commit()
            print(f"Data successfully inserted into '{table_name}' with returning ID: {inserted_id}")
            return inserted_id
        except psycopg2.IntegrityError:
            self.connection.rollback()
            print(f"Duplicate data found in '{table_name}', skipping insertion.")
            return None
        except psycopg2.Error as err:
            self.connection.rollback()
            print(f"Error inserting data in '{table_name}': {err}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_tables_sizes_from_db(self) -> dict:
        """
        Retrieves the sizes of tables in the public schema of the database.

        Returns:
            dict: A dictionary where keys are table names and values are their sizes
            exp:
            Table sizes in the database <fly_tickets_db>:
                {'ticket_prices_history': '40 kB',
                'flight': '32 kB', 'route': '16 kB',
                'departure_airport': '8192 bytes',
                'city': '8192 bytes',
                'arrival_airport': '8192 bytes'}
        """
        try:
            cursor = self.connection.cursor()
            db_name = self.connection.get_dsn_parameters().get('dbname')
            query = """
                SELECT relname AS table_name,
                    pg_size_pretty(pg_relation_size(quote_ident(relname))) AS size
                FROM pg_stat_user_tables
                ORDER BY pg_relation_size(quote_ident(relname)) DESC
            """
            cursor.execute(query)
            table_sizes = {row[0]: row[1] for row in cursor.fetchall()}
            print(f"Table sizes in the database <{db_name}>: {table_sizes}")
            return table_sizes
        except psycopg2.Error as err:
            print(f"Error querying table sizes: {err}")
            return {}
        finally:
            if cursor:
                cursor.close()

    def get_existing_tables_from_db(self) -> list:
        """
        Retrieves the list of existing table names in the database.
        Returns:
            list: List of table names in the public schema.
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
            print(f"Existing tables in the database: <{db_name}>, tables: {existing_tables}")
            return existing_tables
        except psycopg2.Error as err:
            print(f"Error querying existing tables: {err}")
            return []
        finally:
            if cursor:
                cursor.close()

    def get_db_connection_parameters(self) -> dict:
        """
        Retrieves the database connection parameters.

        Returns:
            dict: Dictionary containing connection parameters.
        """
        try:
            dsn_params = self.connection.get_dsn_parameters()
            print(f"DSN Parameters: {dsn_params}")
            return dsn_params
        except psycopg2.Error as err:
            print(f"Error retrieving DSN parameters: {err}")
            return None


class CityDataInserter(DataBaseInsertion):
    """
    A class for inserting and retrieving city data in the database.
    """

    def insert_to_city(self, city_name, city_code, country_code) -> int:
        """
        Inserts city data if it doesn't exist, and returns the city_id.
        Args:
            city_name (str): The name of the city.
            city_code (str): The unique code of the city.
            country_code (str): The country code of the city.
        Returns:
            (int) The city_id if inserted or found, otherwise None.
        """
        city_id = self.get_existing_city_id(city_name, city_code, country_code)
        if city_id:
            return city_id

        _query_insert = """
            INSERT INTO city (
                city_name,
                code,
                country_code
            )
            VALUES (%s, %s, %s)
            RETURNING city_id;
        """
        _city_data = (city_name, city_code, country_code)
        _table_name = 'city'
        new_city_id = self.insert_data_returning_id(_query_insert, _city_data, _table_name)
        return new_city_id

    def extract_city_depart_data(self, flight_data: FlightData) -> tuple:
        """
        Extracts city data for the departure city.
        Args:
            flight_data (FlightData): Flight data object containing departure details.
        Returns:
            tuple: A tuple containing (city_name, city_code, country_code).
                   Example: ('Kaunas', 'KAUNAS', 'LT')
        """
        city_depart_tuple = (
            flight_data.get_departure_city_name(),
            flight_data.get_departure_city_code(),
            flight_data.get_departure_country_code(),
        )
        return city_depart_tuple

    def extract_city_arrival_data(self, flight_data: FlightData) -> tuple:
        """
        Extracts city data for the arrival city.
        Args:
            flight_data (FlightData): Flight data object containing arrival details.
        Returns:
            tuple: A tuple containing (city_name, city_code, country_code).
                   Example: ('Palma', 'PALMA', 'ES')
        """
        city_arrival_tuple = (
            flight_data.get_arrival_city_name(),
            flight_data.get_arrival_city_code(),
            flight_data.get_arrival_country_code(),
        )
        return city_arrival_tuple

    def get_existing_city_id(self, city_name, city_code, country_code) -> int | None:
        """
        Checks if a city exists in the database and returns its city_id.
        Args:
            city_name (str): The name of the city.
            city_code (str): The unique city code.
            country_code (str): The country code.
        Returns:
            int | None: The city_id if found, otherwise None.
        """
        _query_existing_city_id = """
            SELECT city_id FROM city
            WHERE city_name = %s AND code = %s AND country_code = %s
        """
        result = self.fetch_one_from_db(_query_existing_city_id, (city_name, city_code, country_code))

        if result:
            city_id = result  # result[0]
            return city_id
        else:
            return None


class DepartureDataInserter(DataBaseInsertion):
    """
    A class responsible for inserting and retrieving departure airport data
    in the database.
    """

    def insert_to_departure_airport(self, flight_data: FlightData)  -> int | None:
        """
        Inserts data into the departure_airport table using the correct fk_city_id.
        If the airport already exists, it retrieves and returns the existing ID.
        Args:
            flight_data (FlightData): An object containing flight departure details.
        Returns:
            int | None: The departure_airport_id if inserted or found, otherwise None.
        """
        city_inserter = CityDataInserter(self.connection)
        city_depart_data = city_inserter.extract_city_depart_data(flight_data)
        city_name, city_code, country_code = city_depart_data
        city_id = city_inserter.insert_to_city(city_name, city_code, country_code)
        if not city_id:
            return None

        query = """
            INSERT INTO departure_airport (
                depart_country_name,
                depart_iata_code,
                depart_airport_name,
                fk_city_id
            ) VALUES (%s, %s, %s, %s)
            RETURNING depart_airport_id;
        """

        _departure_data_tuple = self._extract_departure_data(flight_data, city_id)
        depart_country_name, depart_iata_code, depart_airport_name, city_id = _departure_data_tuple

        db_depart_id = self.get_depart_airport_id_from_db(depart_iata_code)
        if db_depart_id:
            return db_depart_id

        _table_name = "departure_airport"
        depart_airport_id = self.insert_data_returning_id(query, _departure_data_tuple, _table_name)
        if depart_airport_id is not None:
            return depart_airport_id
        else:
            print("Error: Unable to retrieve departure airport ID.")


    def _extract_departure_data(self, flight_data: FlightData, city_id: int) -> tuple:
        """
        Extracts and returns departure airport data, including the foreign key city_id.
        Args:
            flight_data (FlightData): An object containing flight departure details.
            city_id (int): The foreign key referencing the city's ID.
        Returns:
            tuple: A tuple containing (depart_country_name, depart_iata_code, depart_airport_name, city_id).
        """
        flight_departure_data_tuple = (
            flight_data.get_departure_country_name(),
            flight_data.get_departure_airport_iata(),
            flight_data.get_departure_airport_name(),
            city_id,
        )
        return flight_departure_data_tuple

    def get_depart_airport_id_from_db(self, depart_iata_code: str) -> int | None:
        """
        Retrieves the departure airport ID from the database based on the IATA code.
        Args:
            depart_iata_code (str): The IATA code of the departure airport.
        Returns:
            int | None: The departure_airport_id if found, otherwise None.
        """
        query = """
            SELECT depart_airport_id
            FROM departure_airport
            WHERE depart_iata_code = %s;
        """
        result = self.fetch_one_from_db(query, (depart_iata_code,))
        return result


class ArrivalDataInserter(DataBaseInsertion):
    """
    A class responsible for inserting and retrieving arrival airport data in the database.
    """

    def insert_to_arrival_airport(self, flight_data: FlightData) -> int | None:
        """
        Inserts data into the arrival_airport table using the correct fk_city_id.
        If the airport already exists, it retrieves and returns the existing ID.
        Args:
            flight_data (FlightData): An object containing flight arrival details.
        Returns:
            int | None: The arrival_airport_id if inserted or found, otherwise None.
        """
        city_inserter = CityDataInserter(self.connection)
        city_arrival_data = city_inserter.extract_city_arrival_data(flight_data)
        city_name, city_code, country_code = city_arrival_data
        city_id = city_inserter.insert_to_city(city_name, city_code, country_code)
        if not city_id:
            return

        query = """
            INSERT INTO arrival_airport (
                arriv_country_name,
                arriv_iata_code,
                arriv_airport_name,
                fk_city_id
            ) VALUES (%s, %s, %s, %s)
            RETURNING arriv_airport_id;
        """
        _arrival_data_tuple = self._extract_arrival_data(flight_data, city_id)
        arriv_country_name, arriv_iata_code, arriv_airport_name, city_id = _arrival_data_tuple

        db_arriv_id = self.get_arriv_airport_id_from_db(arriv_iata_code)
        if db_arriv_id:
            return db_arriv_id

        _table_name = "arrival_airport"

        arriv_airport_id = self.insert_data_returning_id(query, _arrival_data_tuple, _table_name)
        if arriv_airport_id is not None:
            return arriv_airport_id
        else:
            print("Error: Unable to retrieve arrival airport ID.")

    def _extract_arrival_data(self, flight_data: FlightData, city_id: int) -> tuple:
        """
        Extracts and returns arrival airport data, including the foreign key city_id.
        Args:
            flight_data (FlightData): An object containing flight arrival details.
            city_id (int): The foreign key referencing the city's ID.
        Returns:
            tuple: A tuple containing (arriv_country_name, arriv_iata_code, arriv_airport_name, city_id).
        """
        flight_arrival_data_tuple = (
            flight_data.get_arrival_country_name(),
            flight_data.get_arrival_airport_iata(),
            flight_data.get_arrival_airport_name(),
            city_id,
        )
        return flight_arrival_data_tuple

    def get_arriv_airport_id_from_db(self, arriv_iata_code: str) -> int | None:
        """
        Retrieves the arrival airport ID from the database based on the IATA code.
        Args:
            arriv_iata_code (str): The IATA code of the arrival airport.
        Returns:
            int | None: The arrival_airport_id if found, otherwise None.
        """
        query = """
            SELECT arriv_airport_id
            FROM arrival_airport
            WHERE arriv_iata_code = %s;
        """
        result = self.fetch_one_from_db(query, (arriv_iata_code,))
        return result


class FlightDataInserter(DataBaseInsertion):
    """
    A class responsible for inserting and updating flight data in the database.
    """

    def insert_to_flight(self, flight_data: FlightData, route_id: int,
                         depart_airport_id: int, arriv_airport_id: int)  -> int | None:
        """
        Inserts flight data into the flight table after getting the route ID.
        If insertion is successful, returns the new flight ID.
        Args:
            flight_data (FlightData): An object containing flight details.
            route_id (int): The foreign key referencing the route_id.
            depart_airport_id (int): The foreign key referencing the departure airport ID.
            arriv_airport_id (int): The foreign key referencing the arrival airport ID.
        Returns:
            int | None: The flight ID if inserted successfully, otherwise None.
        """
        query = """
            INSERT INTO flight (
                fk_route_id,
                fk_depart_airport_id,
                fk_arriv_airport_id,
                departure_date,
                arrival_date,
                ticket_price,
                flight_number,
                price_updated_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING flight_id;
        """

        flight_data_tuple = self._extract_flight_data(flight_data, route_id,
                                                    depart_airport_id,
                                                    arriv_airport_id)
        table_name = "flight"
        flight_id = self.insert_data_returning_id(query, flight_data_tuple, table_name)

        if flight_id is not None:
            return flight_id
        else:
            print(f"Error: Unable to insert flight data with ID: {flight_id}")

    def _extract_flight_data(self, flight_data: FlightData,
                            route_id: int,
                            depart_airport_id: int,
                            arrival_airport_id: int) -> tuple:
        """
        Extracts flight data and returns a tuple data.
        Args:
            flight_data (FlightData): An object containing flight details.
            route_id (int): The foreign key referencing the route ID.
            depart_airport_id (int): The foreign key referencing the departure airport ID.
            arriv_airport_id (int): The foreign key referencing the arrival airport ID.
        Returns:
            tuple: A tuple containing all necessary flight details for database insertion.
        """
        flight_data_tuple = (
            route_id,
            depart_airport_id,
            arrival_airport_id,
            flight_data.get_departure_date(),
            flight_data.get_arrival_date(),
            flight_data.get_latest_price(),
            flight_data.get_flight_number(),
            flight_data.get_price_updated_dates(),
        )
        return flight_data_tuple

    def update_flight_db_ticket_price(self, flight_id: int, new_price: float, price_updated_date: str) -> bool:
        """
        Updates the ticket price and price update date for a specific flight.
        Args:
            flight_id (int): The ID of the flight whose price needs to be updated.
            new_price (float): The new ticket price.
            price_updated_date (str): The date when the price was last updated.
        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = """
            UPDATE flight
            SET ticket_price = %s, price_updated_date = %s
            WHERE flight_id = %s;
        """
        values = (new_price, price_updated_date, flight_id)
        _table_name = "flight"
        result = self.update_data_in_db(query, values,  _table_name)

        if result:
            print(f"Ticket price updated for flight ID {flight_id}: {new_price} on {price_updated_date}")
        else:
            print(f" Failed to update ticket price for flight ID {flight_id}")


class PricesHistoryDataInserter(DataBaseInsertion):
    """
    A class responsible for inserting price history data into the ticket_prices_history table.
    """

    def insert_to_prices_history(self, flight_data: FlightData, flight_id: int) -> int | None:
        """
        Inserts price history data into the ticket_prices_history table.
        Args:
            flight_data (FlightData): An object containing flight price history details.
            flight_id (int): The foreign key referencing the flight ID.
        Returns:
            int | None: The inserted ticket price history ID if successful, otherwise None.
        """
        if not flight_id:
            return None

        _query = """
            INSERT INTO ticket_prices_history (
                fk_flight_id,
                price,
                currency_code,
                price_added_date
            ) VALUES (%s, %s, %s, %s)
        """
        _history_data_tuple = self._extract_prices_history_data(flight_data, flight_id)
        _table_name = "ticket_prices_history"

        ticket_id = self.insert_data_to_db(_query, _history_data_tuple, _table_name)
        return ticket_id

    def _extract_prices_history_data(self, flight_data: FlightData, flight_id: int) -> tuple:
        """
        Extracts and returns price history data including foreign key IDs.
        Args:
            flight_data (FlightData): An object containing flight price details.
            flight_id (int): The foreign key referencing the flight ID.
        Returns:
            tuple: A tuple containing all necessary price history details for database insertion.
        """
        price_data_tuple = (
            flight_id,
            flight_data.get_latest_price(),
            flight_data.get_currency_code(),
            flight_data.get_latest_prices_timestamp(),
        )
        return price_data_tuple


class RouteTableDataInserter(DataBaseInsertion):
    """
    A class responsible for inserting route data into the route table.
    """

    def insert_to_route(self, depart_airport_id: int, arriv_airport_id: int, flight_data: FlightData) -> int | None:
        """
        Inserts data into the route table using the correct foreign keys for departure and arrival airports.
        Args:
            flight_data (FlightData): The flight data object containing flight details.
            depart_airport_id (int): The foreign key referencing the departure airport.
            arriv_airport_id (int): The foreign key referencing the arrival airport.
        Returns:
            int | None: The inserted route ID if successful, otherwise None.
        """
        if depart_airport_id is None or arriv_airport_id is None:
            print("Error: Unable to retrieve airport IDs for route insertion.")
            return None

        _query_route = """
            INSERT INTO route (
                fk_depart_airport_id,
                fk_arriv_airport_id,
                flight_number
            ) VALUES (%s, %s, %s)
            RETURNING route_id;
        """

        _route_data_tuple = self._extract_route_data(flight_data, depart_airport_id, arriv_airport_id)
        _table_name = "route"
        route_id = self.insert_data_returning_id(_query_route, _route_data_tuple, _table_name)
        if route_id is not None:
            return route_id
        else:
            print("Error: Failed to insert route data.")

    def _extract_route_data(self, flight_data: FlightData, departure_airport_id: int, arrival_airport_id: int):
        """
        Extracts route data as a tuple for insertion.
        Args:
            flight_data (FlightData): The flight data object.
            depart_airport_id (int): The departure airport ID.
            arriv_airport_id (int): The arrival airport ID.
        Returns:
            tuple: A tuple containing the departure airport ID, arrival airport ID, and flight number.
        """
        return (
            departure_airport_id,
            arrival_airport_id,
            flight_data.get_flight_number(),
        )


class LatestPriceFromHistoryData(DataBaseInsertion):
    """
    A class to fetch the latest ticket price from the ticket_prices_history table.
    """

    def get_db_latest_ticket_price(self, flight_id: int) -> float:
        """
        Fetches the latest price entry for a given flight_id from ticket_prices_history
        by using the most recent price_added_date column.
        Args:
            flight_id (int): The flight ID from the flight table.
        return: float value
        """
        _query = """
            SELECT price, currency_code, price_added_date
            FROM ticket_prices_history
            WHERE fk_flight_id = %s
            ORDER BY price_added_date DESC
            LIMIT 1
        """
        latest_price_result = self.fetch_one_from_db(_query, (flight_id,))
        return latest_price_result


class PriceHistoryDataRowInserter(DataBaseInsertion):
    """
    Handles inserting new price history records for existing flights in ticket_prices_history.
    """

    def insert_row_price_history(self, flight_id: int, price: float, currency: str, timestamp: str) -> bool:
        """
        Inserts a new row into the `ticket_prices_history` table for an existing flight.
        Ensures that only existing flights get price history updates.
        Args:
            flight_id (int): The ID of the flight from the flight table.
            price (float): The latest price to be recorded.
            currency (str): The currency code (e.g., "USD", "EUR").
            timestamp (str): The timestamp of the price update.
        Returns:
            bool: True if insertion was successful, False otherwise.
        """
        if not flight_id:
            return None

        _query = """
            INSERT INTO ticket_prices_history (
                fk_flight_id,
                price,
                currency_code,
                price_added_date
            ) VALUES (%s, %s, %s, %s)
        """
        _data_tuple = (flight_id, price, currency, timestamp)
        _table_name = "ticket_prices_history"

        success = self.insert_data_to_db(_query, _data_tuple, _table_name)
        if success:
            return True
        else:
            return False


class TicketDataDb(DataBaseInsertion):
    """
    Handles fetching ticket-related data from the database.
    """

    def _query_get_ticket_data(self, values) -> List[Tuple]:
        """
        Queries the database for ticket data matching specific flight criteria.
        Args:
            values (Tuple): A tuple containing flight search parameters.
        Returns:
            List[Tuple]: A list of tuples with ticket data.
            exp: [(210, '2025-05-06 18:25:00', '2025-05-06 21:50:00', 'FR5502', 'KUN  ', 'AGP')]
        """
        _query = """
            SELECT
                f.flight_id,
                f.departure_date,
                f.arrival_date,
                f.flight_number,
                da.depart_iata_code,
                aa.arriv_iata_code
            FROM flight f
            JOIN departure_airport da ON f.fk_depart_airport_id = da.depart_airport_id
            JOIN arrival_airport aa ON f.fk_arriv_airport_id = aa.arriv_airport_id
            WHERE
                f.flight_number = %s AND
                f.departure_date = %s AND
                f.arrival_date = %s AND
                da.depart_iata_code = %s AND
                aa.arriv_iata_code = %s
        """
        if not isinstance(values, tuple):
            values = (values,)

        ticket_data = self.fetch_data_from_db(_query, values)
        return ticket_data

    def get_ticket_data(self, flight_data) -> List[Tuple]:
        """
        Retrieves ticket data from the database based on flight details.
        Args:
            flight_data (FlightData): An object containing flight details.
        Returns:
            List[Tuple]: Ticket data retrieved from the database.
        """
        flight_data_tuple = self._extract_json_data(flight_data)
        db_ticket_data = self._query_get_ticket_data((flight_data_tuple))
        return  db_ticket_data

    def _extract_json_data(self, flight_data: FlightData)  -> Tuple:
        """
        Extracts relevant flight data into a tuple for database querying.
        Args:
            flight_data (FlightData): An object containing flight details.
        Returns:
            Tuple: A tuple containing flight details for the query.
        """
        flight_data_tuple = (
            flight_data.get_flight_number(),
            flight_data.get_departure_date(),
            flight_data.get_arrival_date(),
            flight_data.get_departure_airport_iata(),
            flight_data.get_arrival_airport_iata(),
        )
        return flight_data_tuple


class RunDataFlightComparison(DataBaseInsertion):
    """
    Compares input JSON flight data with existing DB data.
    - If all values match, do nothing.
    - If only the price is different, insert into `ticket_price_history`.
    - If any other values are different, insert a new flight record.
    """

    def compare_and_insert(self, flight_data: FlightData):
        flight_number = flight_data.get_flight_number()
        depart_iata_code = flight_data.get_departure_airport_iata()
        arriv_iata_code = flight_data.get_arrival_airport_iata()
        new_price = flight_data.get_latest_price()
        departure_date = flight_data.get_departure_date()
        arrival_date = flight_data.get_arrival_date()
        currency_code = flight_data.get_currency_code()
        price_timestamp = flight_data.get_latest_prices_timestamp()
        price_updated = flight_data.get_price_updated_dates()

        ticket_data = TicketDataDb(self.connection)
        db_ticket_data = ticket_data.get_ticket_data(flight_data)

        if isinstance(db_ticket_data, list) and len(db_ticket_data) == 0:
            departure_airport_inserter = DepartureDataInserter(self.connection)
            depart_airport_id = departure_airport_inserter.insert_to_departure_airport(flight_data)

            arrival_airport_inserter = ArrivalDataInserter(self.connection)
            arriv_airport_id = arrival_airport_inserter.insert_to_arrival_airport(flight_data)

            route_inserter = RouteTableDataInserter(self.connection)
            route_id = route_inserter.insert_to_route(depart_airport_id, arriv_airport_id, flight_data)

            flight_inserter = FlightDataInserter(self.connection)
            flight_id = flight_inserter.insert_to_flight(flight_data,
                                                         route_id,
                                                         depart_airport_id,
                                                         arriv_airport_id)

            price_history_inserter = PricesHistoryDataInserter(self.connection)
            price_history_inserter.insert_to_prices_history(flight_data, flight_id)
            return

        db_flight_id, db_departure, db_arrival, db_flight_number, db_depart_iata, db_arriv_iata = db_ticket_data[0]
        db_price_retriever = LatestPriceFromHistoryData(self.connection)
        db_latest_price = db_price_retriever.get_db_latest_ticket_price(db_flight_id)

        if all((
            db_latest_price != new_price,
            db_departure == departure_date,
            db_arrival == arrival_date,
            db_flight_number == flight_number,
            db_depart_iata.strip() == depart_iata_code.strip(),
            db_arriv_iata.strip() == arriv_iata_code.strip(),
        )):
            print(f"Price change detected. Inserting new price {new_price}"
                  f" for flight {flight_number}"
                  f" data row into history.")
            price_row_insert = PriceHistoryDataRowInserter(self.connection)
            price_row_insert.insert_row_price_history(db_flight_id,
                                                    new_price,
                                                    currency_code,
                                                    price_timestamp)
            price_date_update =  FlightDataInserter(self.connection)
            price_date_update.update_flight_db_ticket_price(db_flight_id,
                                                            new_price,
                                                            price_updated)
            return
        else:
            print(f"No changes detected for flight {flight_number}"
                  f"({depart_iata_code} → {arriv_iata_code}). Skipping insert.")
            return

def insert_data_to_db_main():
    """
    Reads flight data from a JSON file, checks if the departure date is more
    recent than yesterday, and inserts it into the database if it meets the criteria.
    Process:
    1. Establish a database connection.
    2. Load flight data from the JSON file.
    3. convert_departure_date_to_timestamp():
        (int) - Convert each flight's departure date to a timestamp.
    4. get_yesterday_timestamp(): (int)- yesterday's timestamp.
    5. If the flight is recent, insert it into the database.
    Returns:
        None
    """
    connection = db_connection(db_params)
    read_json = read_load_json_file(LT_SPAIN_DATA_JSON_PATH)
    for flight in read_json:
        flight_data = FlightData(flight)
        yesterday_day = get_yesterday_timestamp()
        price_updated = flight_data.convert_departure_date_to_timestamp()
        if price_updated and price_updated > yesterday_day:
            flight_for_compa = RunDataFlightComparison(connection)
            flight_for_compa.compare_and_insert(flight_data)
        else:
            continue
    print("Done!")
