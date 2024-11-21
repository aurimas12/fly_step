import pandas as pd
from pathlib import Path
import json
from typing import Dict, List, Any
import logging
import logging.config
from logging_config import LOGGING_CONFIG

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
        print(f"Directory '{directory_path}' created.")
        return True
    else:
        logger.info(f"Directory '{directory_path}' already exists.")
        print(f"Directory '{directory_path}' already exists.")
        return False


def get_price_from_entry(entry: dict) -> float:
    """
    Retrieve the price value from an entry. Returns 0.0 if price is not found or is invalid.
    Args:
        entry (dict): The entry containing the price information.
    Returns:
        float: The price value, or 0.0 if price is not found.
    """
    price = entry.get("price", {}).get("value")
    if price is None or not isinstance(price, (int, float)):
        logger.warning(f"Price not found or invalid in entry: {entry}")
        return 0.0
    return price


def overwrite_existing_entry(existing_item: dict,
                            new_entry: dict,
                            new_price: float,
                            old_price: float):
    """
    Overwrite the price in an existing entry with the price from the new entry.
    Args:
        existing_item (dict): The existing entry to be updated.
        new_entry (dict): The new entry containing the updated price.
        new_price (float): the price from new entry
        old_price: float the price from existinf item
    """

    if isinstance(new_price, (int, float)):
        existing_item["price"] = new_entry["price"]
        logger.info(f"Updated price from {old_price} to {new_price} in entry.")
    else:
        logger.warning("Invalid price value in new entry. Price was not updated.")


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


def check_if_entry_exists(new_entry_data: dict, existing_data: list) -> dict | None:
    """
    Checks if an entry with matching `departureAirport.iataCode`, `arrivalAirport.iataCode`,
    and `departureDate` already exists in the provided list of existing data.
    Args:
        new_entry (dict): The new entry to check.
        existing_data (list): The list of existing entries.
    Returns:
        dict | None: The matching existing entry if found, otherwise `None`.
    """
    for existing_item in existing_data:
        if all([
            existing_item.get("departureAirport", {}).get("iataCode") == new_entry_data.get("departureAirport", {}).get("iataCode"),
            existing_item.get("arrivalAirport", {}).get("iataCode") == new_entry_data.get("arrivalAirport", {}).get("iataCode"),
            existing_item.get("departureDate") == new_entry_data.get("departureDate")
        ]):
            logger.info(f"Matching entry found.")
            return existing_item

    logger.info("No matching entry found.")
    return None


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


def check_update_or_write_data_to_json_file(data: str, json_file_path: str) -> str:
    """
    Checks if the specified data entry already exists in the JSON file.
    If it exists with a different price, updates it. If it doesn't exist,
    appends the new entry.
    Args:
        data (str): JSON string representing the data entry to be added or checked.
        json_file_path (str): Path to the JSON file.
    Returns:
        str: Message indicating if data was added, updated, or if the file was created.
    """
    new_entry = parse_json_safely(data)
    existing_data = read_load_json_file(json_file_path)
    existing_entry = check_if_entry_exists(new_entry, existing_data)

    if existing_entry:
        old_price = get_price_from_entry(existing_entry)
        new_price = get_price_from_entry(new_entry)

        if new_price != old_price:
            overwrite_existing_entry(existing_entry, new_entry, new_price, old_price)
            write_data_to_json_file(existing_data, json_file_path)
            return f"Updated entry {old_price} with new price: {new_price}."
        else:
            logger.info("No update needed. The price is the same.")
            return f"No update needed. The price is the same {new_price}."

    else:
        existing_data.append(new_entry)
        write_data_to_json_file(existing_data, json_file_path)
        return f"Created new entry and added to '{json_file_path}'."


def read_csv_file(csv_file_path: str) -> str:
    """
    function read data from csv file
    Args:
        csv_file_path: (str) path to csv file
    Returns:
        pandas.DataFrame: DataFrame containing the data read from the CSV file
        Returns None if file does not exist or cannot be read
    """
    try:
        df = pd.read_csv(csv_file_path)
        logger.info(f"Successfully read CSV file: '{csv_file_path}'")
        return df
    except FileNotFoundError:
        logger.error(f"Error: CSV file '{csv_file_path}' does not exist.")
        print(f"Error: csv file '{csv_file_path}' does not exist.")
        return None
    except pd.errors.ParserError as e:
        logger.error(f"Error reading CSV file '{csv_file_path}': {e}")
        print(f"Error reading csv file '{csv_file_path}' error: {e}")
        return None


def get_dict_from_csv_df_selected_line(df: pd.DataFrame, search_iata_code: str) -> dict:
    """
    Retrieve a dictionary representation of a specific row from a DataFrame based on a given IATA code.
    Parameters:
    df (pd.DataFrame): The DataFrame containing airport data.
    search_iata_code (str): The IATA code to search for in the DataFrame exp: 'VNO'.
    Returns:
    Dict[str, any]: A dictionary of selected columns from the matching row for the specified IATA code.
                    If the IATA code is not found, an empty dictionary is returned.
    Raises:
    IndexError: If the specified IATA code is found but no rows match the selected columns.
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
    return row_dict


def get_value(data: dict, key: str) -> str:
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
