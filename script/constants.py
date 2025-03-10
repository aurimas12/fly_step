# Urls
BASE_URL = "https://services-api.ryanair.com/farfnd/v4/oneWayFares"

# load_dotenv
LOAD_DOTENV_PATH = './script/db/.env'

# Paths
CSV_AIRPORTS_FILE_PATH = "./script/airports.csv"
VNO_BCN_DATA_JSON_PATH = "./script/data/vno_bcn_data.json"
LT_SPAIN_DATA_JSON_PATH = "./script/data/lt_spain_data.json"
DATA_FOLDER_PATH = "./script/data"

# Paths using in logging_config.py
LOGS_FILE_PATH = "./script/logs/logs_all.log"
LOGS_WARNINGS_FILE_PATH = "./script/logs/logs_warning.log"

# Routes from Lt to Spain used in ryanair_one_way_cheap.py
FLYGHT_ROUTES = [
    {"departure": "VNO", "arrival": "BCN"},
    {"departure": "KUN", "arrival": "ALC"},
    {"departure": "KUN", "arrival": "MAD"},
    {"departure": "KUN", "arrival": "PMI"},
    {"departure": "KUN", "arrival": "AGP"},
]

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
