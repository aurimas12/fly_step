import json
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from constants import base_url, flight_json_schema, vno_bcn_data_json_path, data_folder_path
from file import check_or_directory_exists
from typing import Dict, Any
import logging
import logging.config
from logging_config import LOGGING_CONFIG
from rich import print
from rich.progress import track
from rich_process import display_chipest_flights_in_table
from json_data_process import (
                            get_sort_json_data_flights,
                            prepare_flight_formated_output,
                            check_append_price_and_write_data_to_json_file,
                            time_stamp,
                            )


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

departure_airport_iata = "VNO"
arrival_airport_iata = "BCN"


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
        logger.error(f"Failed to fetch flight data from {departure_iata}"
                    f"to {arrival_iata} on {date_str}: {e}")
        print(f"An error occurred: {e}")
        return None


def get_flight_values_from_data(one_flight_data: Dict[str, Any],
                                json_schema: Dict[str, Any]) -> str:
    """
    Extracts flight information from the provided flight data and updates the
    given JSON structure with this information.
    Args:
        one_flight_data (Dict[str, Any]):
            A dictionary containing details of a flight, including fare
            information, departure and arrival airport details, and flight schedule.
        json_schema (Dict[str, Any]):
            A dictionary structure that will be updated with the extracted flight values.
    Returns:
        str: A JSON-formatted string representing the updated JSON structure,
             including the extracted flight information.
    Raises:
        KeyError: If the expected keys are not present in the `one_flight_data`.
    """
    fares = one_flight_data.get("fares", list)
    if not fares:
        logger.info(f"No fares found in the response data.")
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
        try:
            json_schema["departureAirport"]["countryName"] = departure_country
            json_schema["departureAirport"]["iataCode"] = departure_iata
            json_schema["departureAirport"]["name"] = departure_city
            json_schema["departureAirport"]["city"]["name"] = departure_city_name
            json_schema["departureAirport"]["city"]["code"] = departure_city_code
            json_schema["departureAirport"]["city"]["countryCode"] = departure_countryCode
            json_schema["arrivalAirport"]["countryName"] = arrival_country
            json_schema["arrivalAirport"]["iataCode"] = arrival_iata
            json_schema["arrivalAirport"]["name"] = arrival_city
            json_schema["arrivalAirport"]["city"]["name"] = arrival_city_name
            json_schema["arrivalAirport"]["city"]["code"] = arrival_city_code
            json_schema["arrivalAirport"]["city"]["countryCode"] = arrival_countryCode
            json_schema["departureDate"] = departure_date
            json_schema["arrivalDate"] = arrival_date
            json_schema["flightNumber"] = flight_number
            new_price_entry = {
                "timestamp": time_stamp(),
                "value": price_value
            }
            json_schema["price"]["values"] = [new_price_entry]
            json_schema["price"]["currencyCode"] = price_currency
            json_schema["priceUpdated"] = [price_updated]
            logger.info("Extracted flight information from response data")
            return json.dumps(json_schema, indent=4)

        except KeyError as e:
            logger.error(f"KeyError encountered: {e}")
            raise
        except TypeError as e:
            logger.error(f"TypeError encountered: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        raise


def get_flights_by_date_range(start_date: datetime,
                              end_date: datetime,
                              departure_airport_iata: str,
                              arrival_airport_iata: str) -> None:
    """
    Retrieves flight information for each date within a specified date range
        and writes the data to a JSON file if available.
    Args:
        start_date (datetime): The starting date of the date range.
        end_date (datetime): The ending date of the date range.
        departure_airport_iata (str): iata code of airport Vilnius exp: "VNO"
        arrival_airport_iata (str): iata code of airport Barcelona exp: "BCN"
    Returns:
        None: The function performs output operations
            (printing and writing to a file) but does not return any values.
    """
    for search_day in track(range((end_date - start_date).days + 1), description='Processing ...'):
        search_date = start_date + timedelta(days=search_day)
        one_way_fares = get_one_way_cheap_flight(base_url,
                                                 departure_airport_iata,
                                                 arrival_airport_iata,
                                                 search_date)
        flight_values = get_flight_values_from_data(one_way_fares, flight_json_schema)
        if not flight_values:
            logger.info(f"No flight data available in {search_date.strftime('%Y-%m-%d')}")
            continue
        else:
            result = check_append_price_and_write_data_to_json_file(flight_values, vno_bcn_data_json_path)
            print(result)
            if result:
                logger.info(f"Flight data successfully saved for {search_date.strftime('%Y-%m-%d')}")
            else:
                logger.error(f"Failed to save flight data for {search_date.strftime('%Y-%m-%d')}")


if __name__ == '__main__':
    print(check_or_directory_exists(data_folder_path))
    start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + relativedelta(months=3)
    get_flights_by_date_range(start_date, end_date, departure_airport_iata, arrival_airport_iata)
    sorted_flights_info = get_sort_json_data_flights(vno_bcn_data_json_path, num_results=15)
    output_chipest_fligts = prepare_flight_formated_output(sorted_flights_info)
    display_chipest_flights_in_table(output_chipest_fligts)
    logger.info("Flight data scraping complete")
