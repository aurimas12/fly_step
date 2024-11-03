import json
import requests
from datetime import datetime, timedelta
from constants import base_url, json_structure, vno_bcn_data_path
from file import check_write_data_to_json_file
from typing import Dict, Any


def get_one_way_cheap_flight(base_url: str,
                             departure_iata: str,
                             arrival_iata: str,
                             date: datetime) -> dict:
    """
    Search the cheapest one-way flight information from a given departure airport
    to an arrival airport on a specified date.

    Args:
        base_url (str): The base URL of the flight API to fetch flight data.
        departure_iata (str): The IATA code for the departure airport.
        arrival_iata (str): The IATA code for the arrival airport.
        date (datetime): The date of departure as a datetime object.

    Returns:
        Dict: A dictionary containing flight data and other response information
            if the request is successful;
        otherwise, returns None in case of an error.
    """
    departure_iata_airport = departure_iata.upper()
    arrival_iata_code = arrival_iata.upper()
    date_str = date.strftime("%Y-%m-%d")
    url = (
        f"{base_url}?"
        f"departureAirportIataCode={departure_iata_airport}&"
        f"arrivalAirportIataCode={arrival_iata_code}&"
        f"outboundDepartureDateFrom={date_str}&"
        f"outboundDepartureDateTo={date_str}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_flight_values_from_data(one_flight_data: Dict[str, Any],
                                json_structure: Dict[str, Any]) -> str:
    """
    Extracts flight information from the provided flight data and updates the given JSON structure with this information.
    Args:
        one_flight_data (Dict[str, Any]): A dictionary containing details of a flight, including fare information,
                                            departure and arrival airport details, and flight schedule.
        json_structure (Dict[str, Any]): A dictionary structure that will be updated with the extracted flight values.
    Returns:
        str: A JSON-formatted string representing the updated JSON structure,
             including the extracted flight information, formatted with an indentation of 4 spaces.
    Raises:
        KeyError: If the expected keys are not present in the `one_flight_data`.
    """

    fares = one_flight_data.get("fares", [])
    if not fares:
        print("No fares found")
    else:
        outbound = fares[0]['outbound']
        departure_country = outbound['departureAirport']['countryName']
        departure_iata = outbound['departureAirport']['iataCode']
        departure_city = outbound['departureAirport']['name']
        departure_city_name = outbound['departureAirport']['city']['name']
        departure_city_code = outbound['departureAirport']['city']['code']
        departure_countryCode = outbound['departureAirport']['city']['countryCode']
        arrival_iata = outbound['arrivalAirport']['iataCode']
        arrival_city = outbound['arrivalAirport']['name']
        arrival_city_name = outbound['arrivalAirport']['city']['name']
        arrival_city_code = outbound['arrivalAirport']['city']['code']
        arrival_countryCode = outbound['arrivalAirport']['city']['countryCode']
        departure_date = outbound['departureDate']
        arrival_date = outbound['arrivalDate']
        arrival_country = outbound['arrivalAirport']['countryName']
        flight_number = outbound['flightNumber']
        price_value = outbound['price']['value']
        price_currency = outbound['price']['currencyCode']
        price_updated = outbound['priceUpdated']

        # Update JSON structure with extracted values
        json_structure["departureAirport"]["countryName"] = departure_country
        json_structure["departureAirport"]["iataCode"] = departure_iata
        json_structure["departureAirport"]["name"] = departure_city
        json_structure["departureAirport"]["city"]["name"] = departure_city_name
        json_structure["departureAirport"]["city"]["code"] = departure_city_code
        json_structure["departureAirport"]["city"]["countryCode"] = departure_countryCode
        json_structure["arrivalAirport"]["countryName"] = arrival_country
        json_structure["arrivalAirport"]["iataCode"] = arrival_iata
        json_structure["arrivalAirport"]["name"] = arrival_city
        json_structure["arrivalAirport"]["city"]["name"] = arrival_city_name
        json_structure["arrivalAirport"]["city"]["code"] = arrival_city_code
        json_structure["arrivalAirport"]["city"]["countryCode"] = arrival_countryCode
        json_structure["departureDate"] = departure_date
        json_structure["arrivalDate"] = arrival_date
        json_structure["flightNumber"] = flight_number
        json_structure["price"]["value"] = price_value
        json_structure["price"]["currencyCode"] = price_currency
        json_structure["priceUpdated"] = [price_updated]
        return json.dumps(json_structure, indent=4)


def get_flights_by_date_range(start_date: datetime, end_date: datetime):
    """
    Retrieves flight information for each date within a specified date range
        and writes the data to a JSON file if available.
    Args:
        start_date (datetime): The starting date of the date range.
        end_date (datetime): The ending date of the date range.
    Returns:
        None: The function performs output operations
            (printing and writing to a file) but does not return any values.
    """
    for i in range((end_date - start_date).days + 1):
        search_date = start_date + timedelta(days=i)
        print(search_date)
        # date_str = current_date.strftime("%Y-%m-%d")
        one_way_fares = get_one_way_cheap_flight(base_url, 'VNO', 'BCN', search_date)
        flight_values = get_flight_values_from_data(one_way_fares, json_structure)
        if not flight_values:
            continue
        else:
            print(check_write_data_to_json_file(flight_values, vno_bcn_data_path))


if __name__ == '__main__':
    start_date = datetime(2024,11,8)
    end_date = datetime(2024,12,31)
    get_flights_by_date_range(start_date, end_date)
