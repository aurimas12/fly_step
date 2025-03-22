from __future__ import annotations
from typing import List
from pydantic import BaseModel


class CityDeparture(BaseModel):
    name: str
    code: str
    countryCode: str


class DepartureAirport(BaseModel):
    countryName: str
    iataCode: str
    name: str
    city: CityDeparture


class CityArrival(BaseModel):
    name: str
    code: str
    countryCode: str


class ArrivalAirport(BaseModel):
    countryName: str
    iataCode: str
    name: str
    city: CityArrival


class PriceValue(BaseModel):
    timestamp: int
    value: float


class Price(BaseModel):
    values: List[PriceValue]
    currencyCode: str


class FlightModel(BaseModel):
    departureAirport: DepartureAirport
    arrivalAirport: ArrivalAirport
    departureDate: str
    arrivalDate: str
    price: Price
    flightNumber: str
    priceUpdated: int


"""
flight_json_schema = {
    "departureAirport": {
        "countryName": "",
        "iataCode": "",
        "name": "",
        "city": {
            "name": "",
            "code": "",
            "countryCode": ""
        }
    },
    "arrivalAirport": {
        "countryName": "",
        "iataCode": "",
        "name": "",
        "city": {
            "name": "",
            "code": "",
            "countryCode": ""
        }
    },
    "departureDate": "",
    "arrivalDate": "",
        "price": {
            "values": [],
            "currencyCode": ""
        },
    "flightNumber": "",
    "priceUpdated": ""
}
"""

"""
    {
        "departureAirport": {
            "countryName": "Lithuania",
            "iataCode": "VNO",
            "name": "Vilnius",
            "city": {
                "name": "Vilnius",
                "code": "VILNIUS",
                "countryCode": "lt"
            }
        },
        "arrivalAirport": {
            "countryName": "Spain",
            "iataCode": "BCN",
            "name": "Barcelona",
            "city": {
                "name": "Barcelona",
                "code": "BARCELONA",
                "countryCode": "es"
            }
        },
        "departureDate": "2025-06-15T05:45:00",
        "arrivalDate": "2025-06-15T08:20:00",
        "price": {
            "values": [
                {
                    "timestamp": 1742243975,
                    "value": 95.57
                },
                {
                    "timestamp": 1742413323,
                    "value": 107.17
                }
            ],
            "currencyCode": "EUR"
        },
        "flightNumber": "FR1787",
        "priceUpdated": 1742197497000
    },
"""
