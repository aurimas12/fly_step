from file import read_load_json_file, write_data_to_json_file
import json
from datetime import datetime
from typing import List, Dict
from flight_data_process import FlightData
from rich import print
import logging
import logging.config
from logging_config import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def time_stamp() -> int:
    """
    Get the current timestamp in seconds (without milliseconds).
    The time format is: YYYY-MM-DD HH:MM:SS
    Returns:
        int: The current timestamp in seconds.
    """
    dt = datetime.now()

    # TODO:patikrinai ar nenukapoja sekundziu geriau kita konverteri naudot
    return int(datetime.timestamp(dt))


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


def add_price_and_timestamp_to_existing_entry_values(existing_item: dict, new_price: float) -> None:
    """
    Add the price from the new entry to the list of prices in the existing entry.
    This function ensures that the price list (`price.values`) exists in the
    existing entry and then appends a new price entry with the
    current timestamp and the new price.
    Args:
        existing_item (dict): The existing flight entry to be updated.
            It should contain a `price` key with a nested `values` list.
        new_price (float): The price from the new entry to add.
            This should be a numeric value (int or float).
    Returns:
        None: This function modifies the `existing_item` dictionary
            in place and does not return any value.
    """
    existing_flight = FlightData(existing_item)

    if not isinstance(new_price, (int, float)):
        logger.warning(f"Invalid price value {new_price}. Price was not added.")
        return

    if "price" not in existing_item or "values" not in existing_item["price"]:
        existing_item["price"] = {"values": []}

    new_price_entry = {"timestamp": time_stamp(), "value": new_price}
    existing_flight.get_price_values().append(new_price_entry)
    logger.info(
        f"Added new price {new_price} with timestamp {new_price_entry} to price list."
    )


def check_append_price_and_write_data_to_json_file(data: str, json_file_path: str) -> str:
    """
    Processes a new flight entry, checks for an existing entry in a JSON file,
    and updates or appends the data accordingly.
    Args:
        data (str): JSON string containing the new flight entry from
        update_one_way_flight_json_schema().
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
            add_price_and_timestamp_to_existing_entry_values(existing_entry, new_price)
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
        return f"Added new entry to {json_file_path}, new price: {new_price}"


def check_if_entry_exists(new_entry_data: dict, existing_data: list[dict]) -> dict | None:
    """
    Checks if an entry with matching `departureAirport iataCode`,
    `arrivalAirport iataCode`, and `departureDate` already exists in the
    provided list of existing data.
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
            logger.info("Matching entry found.")
            return existing_item

    logger.info("No matching entry found.")
    return None


def get_sort_json_data_flights(path_to_json: str, num_results: int=5) -> List[Dict]:
    """
    Filters and sorts flight data from a JSON file based on departure date and price.
    Args:
        path_to_json (str): Path to the JSON file containing flight data.
        num_results (int): Number of top cheapest flights to return. Defaults to 5.
    Returns:
        List[Dict]:
            A list of dictionaries representing the sorted flight data.
            Each dictionary contains the original JSON structure of a flight.
    Note:
        - Only flights departing today or in the future are considered.
        - Flights are sorted by the latest price.
        - The function returns up to `num_results` default=5 flights.
    """
    flights_data = read_load_json_file(path_to_json)
    today_date = datetime.today().date()

    filtered_flights_list_of_dict = []

    for entry in flights_data:
        try:
            flight = FlightData(entry)
            departure_date_str = flight.get_departure_date()
            departure_date = datetime.fromisoformat(departure_date_str).date()
            if departure_date >= today_date:
                filtered_flights_list_of_dict.append(entry)
        except Exception as e:
            logger.warning(f"Skipping invalid flight entry: {e}")
            continue

    sorted_flights = sorted(
        filtered_flights_list_of_dict,
        key=lambda x: x["price"]["values"][-1]["value"]
    )
    sorted_flights = sorted_flights[:num_results]
    return sorted_flights


def prepare_flight_formated_output(flights: List[Dict]) -> List[Dict[str, str]]:
    """
    Prepares and formats flight data into a readable output format for display.
    Args:
        flights (List[Dict]):
            A list of sorted flight dictionaries, from `get_sort_json_data_flights`.
    Returns:
        List[Dict[str, str]]:
            A list of dictionaries containing formatted flight data. Each dictionary includes:
                - 'departureDate' (str): Formatted departure date (YYYY-MM-DD HH:MM:SS).
                - 'from' (str): Departure city name.
                - 'to' (str): Arrival city name.
                - 'direction' (str): Route in "City (IATA) -> City (IATA)" format.
                - 'price' (float): Latest flight price.
    Note:
        - The function uses the `FlightData` class to transform each flight entry.
    """
    output_list_of_dict = []
    for i in flights:
        flight = FlightData(i)
        output_list_of_dict.append(flight.to_table_formated_dict())
    return output_list_of_dict
