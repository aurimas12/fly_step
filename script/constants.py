csv_file_path = "./script/data/airports.csv"

base_url = "https://services-api.ryanair.com/farfnd/v4/oneWayFares"

vno_bcn_data_path = "./script/data/vno_bcn_data.json"

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
