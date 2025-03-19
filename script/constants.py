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
    #{"departure": "KUN", "arrival": "ALC"},
    #{"departure": "KUN", "arrival": "MAD"},
    #{"departure": "KUN", "arrival": "PMI"},
    #{"departure": "KUN", "arrival": "AGP"},
]

# Number of months to scraping use in script/ryanair_one_way_cheap.py
GET_DATA_MONTHS = 3

# Number of lines otput in terminal table use in script/ryanair_one_way_cheap.py
OUT_NUM_IN_TABLE = 20

# Scheduler starting time use in script/scripts_scheduler.py
TIME_SETTINGS = [
    (1, 40), (1, 41),
    (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 49),
    (10, 0), (10, 19),
    (11, 58), (11, 59),
    (12, 24), (12, 25), (12, 26),
    (13, 55), (13, 56),
    (14, 49), (14, 50),
    (16, 0),
    (17, 0),
    (18, 0),
    (19, 0), (19, 22),
    (20, 23), (20, 30), (20, 40),(20, 54),
    (21, 5), (21, 20), (21, 42),
    (22, 5), (22, 43),
    (23, 0),
    (0, 22), (0, 26), (0, 48), (0, 49),
]
