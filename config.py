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
        'add_account': "Попробуй добавить новые аккаунты при помощи кнопки 'Добавить'\n<code>Здесь будет ссылка с инструкцией где взять апи ключ</code>",
        'cabinet': 'Кабинет',
        'faq': 'База данных',
        'add_account_btn': 'Добавить аккаунт',
        'add_account_descr': 'Отправь мне токен от своего аккаунта',
        'account_added': "Окей, я добавил этот аккаунт. Он будет называться {account_name}\nАвтоматически подключил такие монеты: {coins_list}\nИзменить их ты сможешь через 'Кабинет'",
        'account_id_invalid': 'Твой апи ключ не валидный или аккаунта с таким ключом не существует, обратись в поддержку или попробуй ещё раз',
        'account_id_already_registered': "Аккаунт с таким апи ключом уже зарегистрирован за вами его имя {account_name}. Проверьте валидность ключа или напишите в поддержку.\nУправление аккаунтом через кнопку 'Кабинет'",
        'again_button': 'Ещё раз',
        'account_cabinet': 'Кабинет аккаунта {account_name}\n\nПодключенные монеты: {coins_list}\n\nЗдесь ты можешь включить или выключить уведомления и посмотреть на статистику аккаунта',
        'change_coins_button': "Изменить список монет",
        'coin_list_descr': "Список подключенных монет для аккаунта {account_name}:",
        'coin_disabled': "Монета выключена ❌",
        'coin_enabled': "Монета включена ✅",
        'workers_stat_button': "Инфо по воркерам",
        'income_stat_button': "Начисления",
        'payouts_stat_button': "Выплаты",
        'notifcation_button': "Оповещения",
        'notification_on': "Оповещения вкл. ✅",
        'notification_off': "Оповещения выкл. ❌",
        'delete_account': "Удалить аккаунт",
        'worker_changed_status': "Воркер {worker_name} изменил статус с ({previous_status}) на ({new_status})",
        'status': {
            -1: "Мёртвый",
            0: "Не активный",
            1: "Активный",
            2: "Нестабильный",
        }
    },
    'en': {
        'hello': "Привет, я бот для мониторинга системы ECMD\n\nКнопка 'Кабинет' для работы с аккаунтами\nКнопка 'База данных' если у тебя есть вопроc",
        'cabinet_msg': "У тебя {account_count} подключенных аккаунтов. Здесь ты можешь управлять подключенными аккаунтами",
        'add_account': "Попробуй добавить новые аккаунты при помощи кнопки 'Добавить'\n<code>Здесь будет ссылка с инструкцией где взять апи ключ</code>",
        'cabinet': 'Cabinet',
        'faq': 'FAQ',
        'add_account_btn': 'Add account',
        'add_account_descr': 'Отправь мне токен от своего аккаунта',
    }
}

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
