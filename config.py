import datetime
from enums.lang import Lang
import os

START_TIME = datetime.datetime.now()
INFLUX_WRITE_TIMEOUT_SEC = 5

POEDITOR_ID = int(os.environ.get('POEDITOR_PROJECT_ID', 0))
POEDITOR_TOKEN = os.environ.get('POEDITOR_TOKEN', '')

CONNECTION_STRING = os.environ.get('CONNECTION_STRING', '')

class InfluxDBParams:
    STATS_DB   = os.environ.get('INFLUXDB_DB', '')
    STATS_HOST = os.environ.get('INFUX_DB_HOST', '')
    STATS_USER = os.environ.get('INFLUXDB_USER', '')
    STATS_PASS = os.environ.get('INFLUXDB_USER_PASSWORD', '')

TOKEN = os.environ.get('TOKEN', '')

ENVIRONMENT = os.environ.get('ENV_NAME', 'debug')

DEFAULT_LANG = Lang.ru

SELECT_COIN_CB = 's_coin'

FALLBACK_CURRENCY = 'USD'

DEFAULT_CURRENCY = 1

# 1 active 0 inactive -1 dead 2 nonstable
WORKER_STATUS_CAROUSEL = {
    3: -1, #all - dead
    -1: 0, #dead - inactive
    0: 1, #inactive - active
    #1: 2, #active - nonstable
    1: 3, #nonstable - all
}

PAYOUTS_CHECK_START_DATETIME = datetime.datetime(2021, 3, 7, 15, 0, 0, 0).timestamp()

PER_PAGE_BLACK_LIST = 6
PER_PAGE_FAQ = 4
PER_PAGE_INCOME = 5
PER_PAGE_PAYOUTS = 3
PER_PAGE_WORKERS = 5
