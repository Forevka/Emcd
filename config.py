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
