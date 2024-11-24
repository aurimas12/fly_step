from file import read_load_json_file
from datetime import datetime
from typing import List, Dict


def prepare_flight_formated_output(flights: List[Dict]) -> List[Dict[str, str]]:
    """
    Prepares and formats flight data into the desired output format,
    including city names and IATA codes, while handling ISO 8601 formatted strings.
    Args:
    from function get_sort_json_data_flights()
    flights (List[Dict]):
        List of flight dictionaries, where each dictionary contains:
            'departureDate' (str): ISO 8601 formatted date and time string
                (e.g., "2024-12-14T05:45:00").
            'departureAirport' (Dict): Dictionary with details of the
                departure city and IATA code.
            'arrivalAirport' (Dict): Dictionary with details of the
                arrival city and IATA code.
            'price' (Dict): Dictionary with flight price information in EUR.
    Returns:
    List[Dict[str, str]]:
        List of formatted flight data, where each dictionary includes:
            'departureDate' (str): Formatted departure date and time
                as "YYYY-MM-DD HH:MM:SS".
            'from' (str): Departure city name (e.g., "Vilnius").
            'to' (str): Arrival city name (e.g., "Barcelona").
            'direction' (str): Direction in "City (IATA) -> City (IATA)" format
                (e.g., "Vilnius (VNO) -> Barcelona (BCN)").
            'price' (float): Price of the flight.
    Note:
        The 'departureDate' is parsed from the ISO 8601 format and
            then reformatted to "YYYY-MM-DD HH:MM:SS".
        Ensure all date strings in the input data comply with the
            ISO 8601 standard to avoid errors.
    """
    output = []
    for flight in flights:
        departure_date = datetime.fromisoformat(flight['departureDate']).strftime('%Y-%m-%d %H:%M:%S')
        departure_city = flight['departureAirport']['city']['name']
        arrival_city = flight['arrivalAirport']['city']['name']
        departure_iata = flight['departureAirport']['iataCode']
        arrival_iata = flight['arrivalAirport']['iataCode']
        price = flight['price']['value']

        direction = f"{departure_city} ({departure_iata}) -> {arrival_city} ({arrival_iata})"

        output.append({
            'departureDate': departure_date,
            'from': departure_city,
            'to': arrival_city,
            'direction': direction,
            'price': price
        })
    return output


def get_sort_json_data_flights(path_to_json: str, num_results: int = 3) -> List[Dict]:
    """
    Filters and sorts flight data from a JSON file based on departure date and price.
    Args:
        path_to_json (str): Path to the JSON file containing flight data.
        num_results (int): Number of top cheapest flights to return. Defaults to 3.
    Returns:
        List[Dict]:
            A list of dictionaries containing the sorted data
    """
    flights_data = read_load_json_file(path_to_json)
    today_date = datetime.today().date()

    filtered_flights = []
    for flight in flights_data:
        departure_date = datetime.fromisoformat(flight['departureDate']).date()
        if departure_date >= today_date:
            filtered_flights.append(flight)

    sorted_flights = sorted(filtered_flights, key=lambda x: x['price']['value'])
    sorted_flights = sorted_flights[:num_results]

    return sorted_flights
