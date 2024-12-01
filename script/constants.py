# Urls
base_url = "https://services-api.ryanair.com/farfnd/v4/oneWayFares"


# Paths
csv_airports_file_path = "./script/airports.csv"
vno_bcn_data_json_path = "./script/data/vno_bcn_data.json"
data_folder_path = "./script/data"
logs_file_path = "./script/logs/logs_all.log"
logs_warning_file_path = "./script/logs/logs_warning.log"


# Json
json_structure = {
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
                "value": [],
                "currencyCode": ""
            },
            "flightNumber": "",
            "priceUpdated": []
        }
