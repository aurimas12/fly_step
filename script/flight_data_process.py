from typing import List, Dict, Union
from datetime import datetime


class FlightData:
    def __init__(self, json_data: Dict):
        """
        Initialize the FlightData object from provided JSON data.
        Args:
            json_data (Dict): JSON data structure containing flight details.
        """
        self.json_data = json_data

    def get_departure_country_name(self) -> str:
        return self.json_data.get("departureAirport", {}).get("countryName", "")

    def get_departure_airport_iata(self) -> str:
        return self.json_data.get("departureAirport", {}).get("iataCode", "")

    def get_departure_airport_name(self) -> str:
        return self.json_data.get("departureAirport", {}).get("name", "")

    def get_departure_city_name(self) -> str:
        return self.json_data.get("departureAirport", {}).get("city", {}).get("name", "")

    def get_departure_city_code(self) -> str:
        return self.json_data.get("departureAirport", {}).get("city", {}).get("code", "")

    def get_departure_country_code(self) -> str:
        return self.json_data.get("departureAirport", {}).get("city", {}).get("countryCode", "")

    def get_departure_date(self, formatted: bool = False) -> Union[str, datetime]:
        departure_date_str = self.json_data.get("departureDate", "")
        try:
            departure_date = datetime.fromisoformat(departure_date_str)
            return departure_date.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return departure_date_str


    def get_arrival_country_name(self) -> str:
        return self.json_data.get("arrivalAirport", {}).get("countryName", "")

    def get_arrival_airport_iata(self) -> str:
        return self.json_data.get("arrivalAirport", {}).get("iataCode", "")

    def get_arrival_airport_name(self) -> str:
        return self.json_data.get("arrivalAirport", {}).get("name", "")

    def get_arrival_city_name(self) -> str:
        return self.json_data.get("arrivalAirport", {}).get("city", {}).get("name", "")

    def get_arrival_city_code(self) -> str:
        return self.json_data.get("arrivalAirport", {}).get("city", {}).get("code", "")

    def get_arrival_country_code(self) -> str:
        return self.json_data.get("arrivalAirport", {}).get("city", {}).get("countryCode", "")

    def get_arrival_date(self, formatted: bool = False) -> Union[str, datetime]:
        arrival_date_str = self.json_data.get("arrivalDate", "")
        try:
            arrival_date = datetime.fromisoformat(arrival_date_str)
            return  arrival_date.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return arrival_date_str


    def get_prices_list(self) -> List[float]:
        """Get the list[float] of price values [76.15, 99.53, 236.77]."""
        return self.json_data.get("price", {}).get("value", [])

    def get_currency_code(self) -> str:
        return self.json_data.get("price", {}).get("currencyCode", "")

    def get_flight_number(self) -> str:
        return self.json_data.get("flightNumber", "")

    def get_price_updated_dates(self) -> List[str]:
        return self.json_data.get("priceUpdated", [])

    def get_latest_price(self) -> float:
        """Get the latest price from the price list.
            price list from def get_prices_list()
        """
        price_list = self.get_prices_list()
        return price_list[-1] if price_list else 0.0


    def get_direction(self) -> str:
        """ Returns(str) direction.
        exp: Vilnius (VNO) -> Barcelona (BCN)
        """
        departure_city = self.get_departure_city_name()
        arrival_city = self.get_arrival_city_name()
        departure_iata = self.get_departure_airport_iata()
        arrival_iata = self.get_arrival_airport_iata()
        return f"{departure_city} ({departure_iata}) -> {arrival_city} ({arrival_iata})"

    def to_table_formated_dict(self) -> Dict[str, Union[str, float]]:
        """
        Returns a (dict) with formatted output for easier processing.
        "departureDate", "from", "to", ("direction" from def get_direction()),"price"
        {
            'departureDate': '2024-12-27 12:55:00',
            'from': 'Vilnius',
            'to': 'Barcelona',
            'direction': 'Vilnius (VNO) -> Barcelona (BCN)',
            'price': 243.9
        }
        """
        return {
            "departureDate": self.get_departure_date(formatted=True),
            "from": self.get_departure_city_name(),
            "to": self.get_arrival_city_name(),
            "direction": self.get_direction(),
            "price": self.get_latest_price(),
        }


    def __repr__(self):
        return (
            f"<FlightData from {self.get_departure_city_name()} ({self.get_departure_city_code()}) "
            f"({self.get_departure_airport_iata()}) "
            f"to {self.get_arrival_city_name()} ({self.get_arrival_city_code()}) "
            f"({self.get_arrival_airport_iata()}) | "
            f"on {self.get_departure_date()} "
            f"Latest price: {self.get_latest_price()} {self.get_currency_code()}>"
        )

    def __str__(self) -> str:
        return (
            f"Flight from {self.get_departure_city_name()} ({self.get_departure_airport_iata()}) "
            f"to {self.get_arrival_city_name()} ({self.get_arrival_airport_iata()}) "
            f"on {self.get_departure_date()} "
            f"Price: {self.get_latest_price()} {self.get_currency_code()}"
        )
