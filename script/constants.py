# Urls
base_url = "https://services-api.ryanair.com/farfnd/v4/oneWayFares"


# Paths
csv_airports_file_path = "./script/airports.csv"
vno_bcn_data_json_path = "./script/data/vno_bcn_data.json"
data_folder_path = "./script/data"
logs_file_path = "./script/logs/logs_all.log"
logs_warning_file_path = "./script/logs/logs_warning.log"


# Json
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


# Scheduler starting time
TIME_SETTINGS = [
    (1, 40), (1, 41), (2, 0), (3, 0), (4, 0),
    (5, 0), (6, 0), (7, 0), (8, 0), (9, 49),
    (10, 0),  (10, 19), (11, 58),(11, 59),
    (12, 24), (12, 25), (12, 26), (13, 55), (13, 56),
    (14, 16), (14, 17),(16, 0),  (17, 0),
    (18, 0), (19, 0), (20, 54), (21, 5),
    (21, 41), (21, 42),
    (22, 5), (22, 43), (23, 0), (0, 22),
    (0, 26), (0, 48), (0, 49),
]


# List of script to run in scrips_scheduler.py
from ryanair_one_way_cheap import main
SCRIPT_FUNCTIONS = [
    main,
    main
]
