from enum import Enum

postgres = {
    'host':     '194.99.21.140',
    'user':     'postgres',
    'password': 'werdwerd2012',
    'database': 'Emcd',
    'port':      5433,
}

TOKEN = "666922879:AAEWkOwKYH-Sz7pBm9fLtXDlDV1fSGiNbwo"


texts = {
    'ru': {
        'hello': "Привет, я бот для мониторинга системы ECMD\n\nКнопка 'Кабинет' для работы с аккаунтами\nКнопка 'База данных' если у тебя есть вопроc",
        'cabinet_msg': "У тебя {account_count} подключенных аккаунтов. Здесь ты можешь управлять подключенными аккаунтами",
        'add_account': "Попробуйте добавить новые аккаунты при помощи кнопки 'Добавить'\n`Здесь будет ссылка с инструкцией где взять апи ключ`",
        'cabinet': 'Кабинет',
        'faq': 'База данных',
        'add_account': 'Добавить аккаунт',
    },
    'en': {
        'hello': "Привет, я бот для мониторинга системы ECMD\n\nКнопка 'Кабинет' для работы с аккаунтами\nКнопка 'База данных' если у тебя есть вопроc",
        'cabinet_msg': "У тебя {account_count} подключенных аккаунтов. Здесь ты можешь управлять подключенными аккаунтами",
        'add_account': "Попробуйте добавить новые аккаунты при помощи кнопки 'Добавить'\n`Здесь будет ссылка с инструкцией где взять апи ключ`",
        'cabinet': 'Cabinet',
        'faq': 'FAQ',
        'add_account': 'Add account',
    }
}

class Lang(Enum):
    ru = 1
    en = 2

DEFAULT_LANG = Lang.ru