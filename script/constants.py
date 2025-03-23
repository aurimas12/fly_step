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
    (1, 0), (1, 10), (1, 20), (1, 30), (1, 40), (1, 50),
    (2, 0), (2, 10), (2, 20), (2, 30), (2, 40), (2, 50),
    (3, 0), (3, 10), (3, 20), (3, 30), (3, 40), (3, 50),
    (4, 0), (4, 10), (4, 20), (4, 30), (4, 40), (4, 50),
    (5, 0), (5, 10), (5, 20), (5, 30), (5, 40), (5, 50),
    (6, 0), (6, 10), (6, 20), (6, 30), (6, 40), (6, 50),
    (7, 0), (7, 10), (7, 20), (7, 30), (7, 40), (7, 50),
    (8, 0), (8, 10), (8, 20), (8, 30), (8, 40), (8, 50),
    (9, 0), (9, 10), (9, 20), (9, 30), (9, 40), (9, 50),
    (10, 0), (10, 10), (10, 20), (10, 30), (10, 40), (10, 50),
    (11, 0), (11, 10), (11, 20), (11, 30), (11, 40), (11, 50),
    (12, 0), (12, 10), (12, 20), (12, 30), (12, 40), (12, 50),
    (13, 0), (13, 10), (13, 20), (13, 30), (13, 40), (13, 50),
    (14, 0), (14, 10), (14, 20), (14, 30), (14, 40), (14, 50),
    (15, 0), (15, 10), (15, 20), (15, 30), (15, 40), (15, 50),
    (16, 0), (16, 10), (16, 20), (16, 30), (16, 40), (16, 50),
    (17, 0), (17, 10), (17, 20), (17, 30), (17, 40), (17, 50),
    (18, 0), (18, 10), (18, 20), (18, 30), (18, 40), (18, 50),
    (19, 0), (19, 10), (19, 20), (19, 30), (19, 40), (19, 50),
    (20, 0), (20, 10), (20, 20), (20, 30), (20, 40), (20, 50),
    (21, 0), (21, 10), (21, 20), (21, 30), (21, 40), (21, 50), 
    (22, 0), (22, 10), (22, 20), (22, 30), (22, 40), (22, 50),
    (23, 0), (23, 10), (23, 20), (23, 30), (23, 40), (23, 50),
    (0, 0), (0, 10), (0, 20), (0, 30), (0, 40), (0, 50),
]
