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
    price: float


class Price(BaseModel):
    prices_history: List[PriceValue]
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
        "departureDate": "2025-03-25T17:05:00",
        "arrivalDate": "2025-03-25T19:40:00",
        "price": {
            "prices_history": [
                {
                    "timestamp": 1742751829,
                    "price": 191.29
                }
            ],
            "currencyCode": "EUR"
        },
        "flightNumber": "FR1787",
        "priceUpdated": 1742734424000
    }
"""
