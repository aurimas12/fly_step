from __future__ import annotations
from typing import List
from pydantic import BaseModel


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
    "priceUpdated": []
}
"""


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
