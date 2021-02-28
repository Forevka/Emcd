import datetime
import os
from enum import Enum

POEDITOR_ID = 418393
POEDITOR_TOKEN = os.environ.get('POEDITOR_TOKEN')

START_TIME = datetime.datetime.now()

postgres = os.environ.get('CONNECTION_STRING')

TOKEN = os.environ.get('TOKEN')

# placeholder for langs
texts = {}
reversed_locales = {}

def update_texts(data: dict):
    global texts, reversed_locales
    texts = data
    for lang_code, terms in texts.items():
        reversed_locales[lang_code] = dict((v.lower(), k.lower()) for k,v in terms.items()) # exchange key with values

class Lang(Enum):
    ru = 1
    en = 2

DEFAULT_LANG = Lang.ru

class Coin(Enum):
    Bitcoin = 'btc'
    BitcoinHash = 'bchn'
    BitcoinSV = 'bsv'
    Litecoin = 'ltc'
    Dash = 'dash'
    Ethereum = 'eth'
    EthereumClassic = 'etc'
