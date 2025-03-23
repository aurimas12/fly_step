import json
import time
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from constants import (
                    BASE_URL, FLYGHT_ROUTES,
                    LT_SPAIN_DATA_JSON_PATH, DATA_FOLDER_PATH,
                    GET_DATA_MONTHS, OUT_NUM_IN_TABLE)
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
                            )
from db.create_tables import create_all_tables_main
from db.json_data_to_db import insert_data_to_db_main
from count_timer import count_timer
from models import (FlightModel, DepartureAirport, ArrivalAirport,
                    CityDeparture, CityArrival, Price, PriceValue)



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
        return response.json()
    except requests.exceptions.RequestException as err:
        logger.error(f"Failed to fetch flight data from {departure_iata}"
                    f"to {arrival_iata} on {date_str}: {err}")
        print(f"An error occurred: {err}")
        return None


def extract_one_way_flight_details(one_flight_data: Dict[str, Any]) -> FlightModel:
    """
    Extracts flight details from the provided flight data into a FlightModel.
    """
    fares = one_flight_data.get("fares", [])
    if not fares:
        logger.info("No fares found in the response data.")
        return None

    outbound = fares[0]['outbound']
    try:
        return FlightModel(
            departureAirport = DepartureAirport(
                countryName = outbound['departureAirport']['countryName'],
                iataCode = outbound['departureAirport']['iataCode'],
                name = outbound['departureAirport']['name'],
                city = CityDeparture(
                    name = outbound['departureAirport']['city']['name'],
                    code = outbound['departureAirport']['city']['code'],
                    countryCode = outbound['departureAirport']['city']['countryCode']
                )
            ),
            arrivalAirport = ArrivalAirport(
                countryName = outbound['arrivalAirport']['countryName'],
                iataCode = outbound['arrivalAirport']['iataCode'],
                name = outbound['arrivalAirport']['name'],
                city = CityArrival(
                    name = outbound['arrivalAirport']['city']['name'],
                    code = outbound['arrivalAirport']['city']['code'],
                    countryCode = outbound['arrivalAirport']['city']['countryCode']
                )
            ),
            departureDate = outbound['departureDate'],
            arrivalDate = outbound['arrivalDate'],
            flightNumber = outbound['flightNumber'],
            price = Price(
                prices_history = [PriceValue(
                    timestamp = int(time.time()),
                    price = outbound['price']['value']
                    )],
                currencyCode = outbound['price']['currencyCode']
            ),
            priceUpdated=outbound['priceUpdated']
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


def update_one_way_flight_json_schema(flight_model: FlightModel) -> str:
    """
    Update and format JSON schema with flight details.
    """
    try:
        json_schema = flight_model.model_dump()
        json_schema['price']['prices_history'] = [
            {
                "timestamp": int(time.time()),
                "price": json_schema['price']['prices_history'][0]['price']
            }
        ]
        json_schema['price']['currencyCode'] = flight_model.price.currencyCode
        json_schema['priceUpdated'] = flight_model.priceUpdated
        logger.info("JSON schema successfully updated.")
        return json.dumps(json_schema, indent=4)
    except Exception as e:
        logger.error(f"Error updating JSON schema: {e}")
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

            updated_json_schema = update_one_way_flight_json_schema(extracted_flight_values)
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


@count_timer
def ryanair_main():
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
    create_all_tables_main()
    insert_data_to_db_main()
