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


def check_write_data_to_json_file(data: str, json_file_path: str) -> str:
    """
    Function creates, check or data exist and adds unique data
        (based on 'iataCode', 'price' and 'departureDate') to a JSON file.
    Args:
        data (str): JSON string representing the data entry to be added
                    or appended to the JSON file.
        json_file_path (str): Path to the JSON file.
    Returns:
        str: A message indicating whether new data was added, no new data was added,
             or the file was created and data was written.
    """
    try:
        new_entry = json.loads(data)
    except json.JSONDecodeError:
        logger.error("Invalid JSON data provided.")
        return "Invalid JSON data provided."

    path = Path(json_file_path)

    if path.is_file():
        with open(path, "r+", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                logger.warning(f"File '{json_file_path}' contained invalid JSON. Overwriting with new data.")
                existing_data = None

            if isinstance(existing_data, list):
                exists = any(
                    isinstance(existing_item, dict) and
                    existing_item.get("departureAirport", {}).get("iataCode") == new_entry.get("departureAirport", {}).get("iataCode") and
                    existing_item.get("arrivalAirport", {}).get("iataCode") == new_entry.get("arrivalAirport", {}).get("iataCode") and
                    existing_item.get("price", {}).get("value") == new_entry.get("price", {}).get("value") and
                    existing_item.get("departureDate") == new_entry.get("departureDate")
                    for existing_item in existing_data
                )

                if exists:
                    logger.info(f"No new data added to '{json_file_path}', it already exists.")
                    return f"No new data added to '{json_file_path}', it already exists."
                else:
                    existing_data.append(new_entry)
                    file.seek(0)
                    json.dump(existing_data, file, indent=4)
                    file.truncate()
                    logger.info(f"New data added to '{json_file_path}'.")
                    return f"New data added to '{json_file_path}'."
            else:
                file.seek(0)
                json.dump([new_entry], file, indent=4)
                file.truncate()
                logger.info(f"File '{json_file_path}' did not contain valid data. Overwritten with new data.")
                return f"File '{json_file_path}' contained invalid data. Overwritten with new data."
    else:
        with open(path, "w", encoding="utf-8") as file:
            json.dump([new_entry], file, indent=4)
            logger.info(f"Created '{json_file_path}' and wrote data to it.")
            return f"Created '{json_file_path}' and wrote data to it."



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
