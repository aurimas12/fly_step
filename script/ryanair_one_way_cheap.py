import json
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from constants import (
                    BASE_URL, FLIGHT_JSON_SCHEMA, FLYGHT_ROUTES,
                    LT_SPAIN_DATA_JSON_PATH, DATA_FOLDER_PATH)
from file import check_or_directory_exists
from typing import Dict, Any, Tuple
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
from config import GET_DATA_MONTHS, OUT_NUM_IN_TABLE


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


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


def extract_one_way_flight_details(one_flight_data: Dict[str, Any]) -> Tuple[Any, ...]:
    """
    Extracts flight details from the provided flight data as separate values
    from get_one_way_cheap_flight().
    Args:
        one_flight_data (Dict[str, Any]): A dictionary containing flight details.
    Returns:
        Tuple[Any, ...]: A tuple of extracted values.
    """
    fares = one_flight_data.get("fares", [])
    if not fares:
        logger.info("No fares found in the response data.")
        return None

    outbound = fares[0]['outbound']
    try:
        departure_country = outbound['departureAirport']['countryName']
        departure_iata = outbound['departureAirport']['iataCode']
        departure_city = outbound['departureAirport']['name']
        departure_city_name = outbound['departureAirport']['city']['name']
        departure_city_code = outbound['departureAirport']['city']['code']
        departure_country_code = outbound['departureAirport']['city']['countryCode']
        arrival_country = outbound['arrivalAirport']['countryName']
        arrival_iata = outbound['arrivalAirport']['iataCode']
        arrival_city = outbound['arrivalAirport']['name']
        arrival_city_name = outbound['arrivalAirport']['city']['name']
        arrival_city_code = outbound['arrivalAirport']['city']['code']
        arrival_country_code = outbound['arrivalAirport']['city']['countryCode']
        departure_date = outbound['departureDate']
        arrival_date = outbound['arrivalDate']
        flight_number = outbound['flightNumber']
        price_value = outbound['price']['value']
        price_currency = outbound['price']['currencyCode']
        price_updated = outbound['priceUpdated']

        return (
            departure_country, departure_iata, departure_city, departure_city_name,
            departure_city_code, departure_country_code, arrival_country, arrival_iata,
            arrival_city, arrival_city_name, arrival_city_code, arrival_country_code,
            departure_date, arrival_date, flight_number, price_value, price_currency,
            price_updated
        )
    except KeyError as e:
        logger.error(f"KeyError encountered during extraction: {e}")
        raise
    except TypeError as e:
        logger.error(f"TypeError encountered during extraction: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during extraction: {e}")
        raise


def update_one_way_flight_json_schema(
    json_schema: Dict[str, Any],
    departure_country: str, departure_iata: str, departure_city: str,
    departure_city_name: str, departure_city_code: str, departure_country_code: str,
    arrival_country: str, arrival_iata: str, arrival_city: str,
    arrival_city_name: str, arrival_city_code: str, arrival_country_code: str,
    departure_date: str, arrival_date: str, flight_number: str,
    price_value: float, price_currency: str, price_updated: str
) -> str:
    """
    Updates the JSON schema with the provided flight details from
    function extract_flight_details().
    Args:
        json_schema (Dict[str, Any]): The JSON structure to update.
        (other params): Individual flight details as separate values.
    Returns:
        str: A JSON-formatted string representing the updated JSON schema.
    """
    try:
        json_schema["departureAirport"] = {
            "countryName": departure_country,
            "iataCode": departure_iata,
            "name": departure_city,
            "city": {
                "name": departure_city_name,
                "code": departure_city_code,
                "countryCode": departure_country_code
            }
        }
        json_schema["arrivalAirport"] = {
            "countryName": arrival_country,
            "iataCode": arrival_iata,
            "name": arrival_city,
            "city": {
                "name": arrival_city_name,
                "code": arrival_city_code,
                "countryCode": arrival_country_code
            }
        }
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

        logger.info("JSON schema successfully updated.")
        json_schema_result = json.dumps(json_schema, indent=4)
        return json_schema_result
    except KeyError as e:
        logger.error(f"KeyError encountered during schema update: {e}")
        raise
    except TypeError as e:
        logger.error(f"TypeError encountered during schema update: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during schema update: {e}")
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
        one_way_fares = get_one_way_cheap_flight(BASE_URL,
                                                 departure_airport_iata,
                                                 arrival_airport_iata,
                                                 search_date)
        try:
            extracted_flight_values = extract_one_way_flight_details(one_way_fares)
            if not extracted_flight_values:
                continue

            updated_json_schema = update_one_way_flight_json_schema(
                FLIGHT_JSON_SCHEMA,
                *extracted_flight_values
            )
            if not updated_json_schema:
                logger.info(f"No flight data available on {search_date.strftime('%Y-%m-%d')}")
                continue

            result = check_append_price_and_write_data_to_json_file(
                updated_json_schema,
                LT_SPAIN_DATA_JSON_PATH
            )
            if result:
                print(search_date.strftime('%Y-%m-%d'), result)
                logger.info(f"Flight data successfully saved for {search_date.strftime('%Y-%m-%d')}")
            else:
                logger.error(f"Failed to save flight data for {search_date.strftime('%Y-%m-%d')}")

        except Exception as e:
            logger.error(f"Unexpected error in def get_flights_by_date_range(): {e}")

def main():
    print(check_or_directory_exists(DATA_FOLDER_PATH))
    start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + relativedelta(months=GET_DATA_MONTHS)

    for route in FLYGHT_ROUTES:
        get_flights_by_date_range(start_date,
                                end_date,
                                route["departure"],
                                route["arrival"]
                                )

    sorted_flights_info = get_sort_json_data_flights(LT_SPAIN_DATA_JSON_PATH, num_results=OUT_NUM_IN_TABLE)
    output_chipest_fligts = prepare_flight_formated_output(sorted_flights_info)
    display_chipest_flights_in_table(output_chipest_fligts)
    logger.info("Flight data scraping complete")

if __name__ == '__main__':
    main()
