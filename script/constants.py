# Urls
BASE_URL = "https://services-api.ryanair.com/farfnd/v4/oneWayFares"


# Paths
CSV_AIRPORTS_FILE_PATH = "./script/airports.csv"
VNO_BCN_DATA_JSON_PATH = "./script/data/vno_bcn_data.json"
DATA_FOLDER_PATH = "./script/data"
LOGS_FILE_PATH = "./script/logs/logs_all.log"
LOGS_WARNINGS_FILE_PATH = "./script/logs/logs_warning.log"


# Json
FLIGHT_JSON_SCHEMA = {
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
