from file import read_load_json_file
from datetime import datetime
from typing import List, Dict
from flight_data_process import FlightData


def get_sort_json_data_flights(path_to_json: str, num_results: int=3) -> List[Dict]:
    """
    Filters and sorts flight data from a JSON file based on departure date and price.
    Args:
        path_to_json (str): Path to the JSON file containing flight data.
        num_results (int): Number of top cheapest flights to return. Defaults to 3.
    Returns:
        List[Dict]:
            A list of dictionaries representing the sorted flight data.
            Each dictionary contains the original JSON structure of a flight.
    Note:
        - Only flights departing today or in the future are considered.
        - Flights are sorted by the latest price in ascending order.
        - The function returns up to `num_results` default=3 flights.
    """
    flights_data = read_load_json_file(path_to_json)
    today_date = datetime.today().date()

    filtered_flights = []
    for entry in flights_data:
        flight = FlightData(entry)
        departure_date_str = flight.get_departure_date()
        departure_date = datetime.fromisoformat(departure_date_str).date()
        if departure_date >= today_date:
            filtered_flights.append(entry)

    sorted_flights = sorted(filtered_flights, key=lambda x: x['price']['value'][-1])
    sorted_flights = sorted_flights[:num_results]
    return sorted_flights


def prepare_flight_formated_output(flights: List[Dict]) -> List[Dict[str, str]]:
    """
    Prepare and format flight data into a readable output format for display.
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
    output = []
    for i in flights:
        flight = FlightData(i)
        output.append(flight.to_table_formated_dict())

    return output
