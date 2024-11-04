# Urls
base_url = "https://services-api.ryanair.com/farfnd/v4/oneWayFares"


# Paths
csv_airports_file_path = "./script/airports.csv"
vno_bcn_data_path = "./script/data/vno_bcn_data.json"
data_folder_path = "./script/data"


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
                "value": None,
                "currencyCode": ""
            },
            "flightNumber": "",
            "priceUpdated": []
        }
