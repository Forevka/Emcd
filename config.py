import datetime
from enums.lang import Lang
import os

START_TIME = datetime.datetime.now()

POEDITOR_ID = 418393
POEDITOR_TOKEN = os.environ.get('POEDITOR_TOKEN')

CONNECTION_STRING = os.environ.get('CONNECTION_STRING')

TOKEN = os.environ.get('TOKEN')

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