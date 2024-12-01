import pandas as pd
from pathlib import Path
import json
from typing import Dict, List, Any
import logging
import logging.config
from logging_config import LOGGING_CONFIG
from flight_data_process import FlightData

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def check_or_directory_exists(directory_path: str):
    """
    Check if a directory exists at the specified path.
    If it does not exist, create it.
    Parameters:
        directory_path (str): The path to the directory to check or create.
    Returns:
        bool: True if the directory was created, False if it already existed.
    """
    path = Path(directory_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory '{directory_path}' created.")
        return f"Directory '{directory_path}' created."
    else:
        logger.info(f"Directory '{directory_path}' already exists.")
        return f"Directory '{directory_path}' already exists."


def write_data_to_json_file(data: list | dict, json_file_path: str) -> str:
    """
    Writes data to a JSON file. If the file does not exist,
    it creates the file and writes the data.
    If the file exists, it append a new data.
    Args:
        data (list | dict): The data to write to the JSON file.
        Can be a list or a dictionary.
        json_file_path (str): The path to the JSON file.
    Returns:
        str: A message indicating whether the file was created or updated.
    """
    path = Path(json_file_path)

    try:
        if isinstance(data, list):
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
                logger.info(f"Data: list successfully written to '{json_file_path}'.")
                return f"Data successfully written to '{json_file_path}'."

        elif isinstance(data, dict):
            with open(path, 'w', encoding='utf-8') as file:
                json.dump([data], file, indent=4)
                logger.info(f"Data: dict successfully written to '{json_file_path}'.")
                return f"Data successfully written to '{json_file_path}'."

        else:
            logger.warning("The provided data must be a list or a dictionary.")
            raise ValueError("The provided data must be a list or a dictionary.")

    except Exception as e:
        logger.error(f"Error writing data to '{json_file_path}': {e}")
        raise


def read_load_json_file(json_file_path: str) -> list:
    """
    Reads JSON data from a file. If the file does not exist, is empty,
    or contains invalid JSON, it returns an empty list without creating a new file.
    Args:
        json_file_path (str): Path to the JSON file.
    Returns:
        list: Parsed JSON data as a list, or an empty list if the file is empty, missing, or invalid.
    """
    path = Path(json_file_path)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
            if data.strip():
                logger.info(f"Successfully loaded data from '{json_file_path}'.")
                return json.loads(data)
            else:
                logger.warning(f"File '{json_file_path}' is empty. Returning an empty list.")
                return []
    except FileNotFoundError:
        logger.warning(f"File '{json_file_path}' not found. Returning an empty list.")
        return []
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON in file '{json_file_path}'. Returning an empty list.")
        return []


def parse_json_safely(data: str) -> dict | None:
    """
    Attempts to parse a string of JSON data. Logs an error if the parsing fails.
    Args:
        data (str): The JSON string to be parsed.
    Returns:
        dict | None: The parsed dictionary if valid JSON, or None if invalid.
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON data: {data[:100]}...")
        return None


def check_if_entry_exists(new_entry_data: dict, existing_data: list) -> dict | None:
    """
    Checks if an entry with matching `departureAirport iataCode`, `arrivalAirport iataCode`,
    and `departureDate` already exists in the provided list of existing data.
    Args:
        new_entry_data (dict): The new entry to check.
        existing_data (list): The list of existing entries.
    Returns:
        dict | None: The matching existing entry if found, otherwise `None`.
    """
    new_flight = FlightData(new_entry_data)

    for existing_item in existing_data:
        existing_flight = FlightData(existing_item)
        if all([
            existing_flight.get_departure_airport_iata() == new_flight.get_departure_airport_iata(),
            existing_flight.get_arrival_airport_iata() == new_flight.get_arrival_airport_iata(),
            existing_flight.get_departure_date() == new_flight.get_departure_date()
        ]):
            return existing_item

    logger.info("No matching entry found.")
    return None


def add_price_to_existing_entry(existing_item: dict, new_price: float) -> None:
    """
    Add the price from the new entry to the list of prices in the existing entry.
    Args:
        existing_item (dict): The existing flight entry to be updated.
        new_price (float): The price from the new entry to add.
    """
    existing_flight = FlightData(existing_item)

    if isinstance(new_price, (int, float)):
        prices_list = existing_flight.get_prices_list()
        if not prices_list:
            prices_list = []

        prices_list.append(new_price)
        logger.info(f"Added new price {new_price} to price list."
                    f"Current prices: {prices_list}")
    else:
        logger.warning(f"Invalid price value {new_price} in the new entry. Price was not added.")


def check_append_price_and_write_data_to_json_file(data: str, json_file_path: str) -> str:
    """
    Processes a new flight entry, checks for an existing entry in a JSON file,
    and updates or appends the data accordingly.
    Args:
        data (str): JSON string containing the new flight entry.
        json_file_path (str): Path to the JSON file containing existing flight data.
    Returns:
        str: A message indicating whether the entry was updated or added.
    Workflow:
        1. Parse the new flight entry from the `data` string.
        2. Load the existing data from the JSON file.
        3. Check if the new entry matches any existing entry
            (based on departure airport, arrival airport, and date).
        4. If a match is found:
            - Check if the new price is already in the price list.
            - If not, add the new price and update the JSON file.
        5. If no match is found:
            - Append the new entry to the existing data and write it back to the file.
    Notes:
        - Uses the `FlightData` class for structured data handling.
        - Updates the `price.value` field of the existing entry if a new price is found.
    """
    new_entry = parse_json_safely(data)
    existing_data = read_load_json_file(json_file_path)
    existing_entry = check_if_entry_exists(new_entry, existing_data)

    if existing_entry:
        existing_flight = FlightData(existing_entry)
        new_flight = FlightData(new_entry)

        all_prices = existing_flight.get_prices_list()
        new_price = new_flight.get_latest_price()

        if new_price not in all_prices:
            add_price_to_existing_entry(existing_entry, new_price)
            write_data_to_json_file(existing_data, json_file_path)
            return f"Updated entry with new price: {new_price} in entry: {all_prices}"
        else:
            logger.info("No update needed. The price is already in the entry.")
            return f"No update needed. The price {new_price} is already in entry: {all_prices}"
    else:
        new_flight = FlightData(new_entry)
        existing_data.append(new_entry)
        write_data_to_json_file(existing_data, json_file_path)
        new_price = new_flight.get_latest_price()
        logger.info(f"Added new entry to JSON, new price: {new_price}")
        return f"Added new entry to JSON, new price: {new_price}"


def get_dict_from_csv_df_selected_line(df: pd.DataFrame, search_iata_code: str) -> dict:
    """
    Retrieve a dictionary representation of a specific row from a DataFrame based
    on a given IATA code.
    Parameters:
        df (pd.DataFrame): The DataFrame containing airport data.
        search_iata_code (str): The IATA code to search exp: 'VNO'.
    Returns:
        Dict[str, any]: A dictionary of selected columns from the matching row
            for the specified IATA code.
            If the IATA code is not found, an empty dictionary is returned.
    Raises:
        IndexError: If the specified IATA code is found but no rows match
        the selected columns.
    """
    selected_columns = [ "id",
                        "icao_code",
                        "type",
                        "name",
                        "latitude_deg",
                        "longitude_deg",
                        "elevation_ft",
                        "continent",
                        "iso_country",
                        "iso_region",
                        "municipality",
                        "scheduled_service",
                        "gps_code",
                        "iata_code",
                        "local_code",
                        "home_link",
                        "wikipedia_link",
                        ]

    search_iata_code = search_iata_code.upper()

    try:
        logger.info(f"Row found for IATA code '{search_iata_code}': {row_dict}")
        row_dict = df[df['iata_code'] == search_iata_code][selected_columns].iloc[0].to_dict()
    except IndexError:
        logger.warning(f"No data found for IATA code '{search_iata_code}'. Returning an empty dictionary.")
        return "Returning an empty dictionary"
    except KeyError as e:
        logger.error(f"DataFrame missing required column: {e}")
        return "DataFrame missing required column"
        #row_dict = {}
    return row_dict


def get_value_from_dict(data: dict, key: str) -> str:
    """
    Retrieve a specific value from a dictionary using a given key.
    Parameters:
    data (row_dict): The dictionary containing the data.
    key (str): The key for which the value is required.
    keys = ["id", "icao_code","type", "name", "latitude_deg","longitude_deg",
            "elevation_ft", "continent","iso_country", "iso_region",
            "municipality", "scheduled_service", "gps_code", "iata_code",
            "local_code", "home_link", "wikipedia_link"]
    Returns (str):
        The value associated with the given key,
        or a message 'none' if the key does not exist.

    Example:
    >>> data = {
            'id': 2766,
            'icao_code': 'EYVI',
            'type': 'large_airport',
            'name': 'Vilnius International Airport'
        }
    >>> get_value(data, 'name')
    'Vilnius International Airport'
    """
    if key in data:
        value = data.get(key)
        logger.info(f"Key '{key}' found in data with value: {value}")
    else:
        value = "none"
        logger.warning(f"Key '{key}' not found in data. Returning default value: {value}")

    return value
