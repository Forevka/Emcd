import datetime
import os
from enum import Enum

START_TIME = datetime.datetime.now()

postgres = os.environ.get('CONNECTION_STRING')

TOKEN = os.environ.get('TOKEN')

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
        'payouts_choose_coin': "Выберите по какой монете вы хотите посмотреть выплаты\nИзменить список монет можно в меню аккаунта",
        'income_choose_coin': "Выберите по какой монете вы хотите посмотреть начисления\nИзменить список монет можно в меню аккаунта",
        'worker_choose_coin': "Выберите по какой монете вы хотите посмотреть статистику воркеров\nИзменить список монет можно в меню аккаунта",
        'notification_choose_coin': "Выберите по какой монете вы хотите изменить настройки уведомлений\nИзменить список монет можно в меню аккаунта",
        'worker_info_descr': "Статистика по воркерам аккаунта {account_name}\nВсего: {total}\nАктивных: {active}\nМёртвых: {dead}\nНеактивных: {inactive}\n{description}",
        'notifcation_button': "Оповещения",
        'notification_on': "Оповещения вкл. ✅",
        'notification_off': "Оповещения выкл. ❌",
        'delete_account': "Удалить аккаунт",
        'worker_changed_status_descr': "{worker_name} - ({previous_status}) на ({new_status})",
        'worker_changed_status_body': "Произошла смена статуса воркеров на аккаунте {account_name}\n\n{description}",
        'status': {
            -1: "Мёртвый",
            0: "Не активный",
            1: "Активный",
            2: "Нестабильный",
        },
        'income_names': {
            "donation": "donation",
            "fpps": "fpps",
            "referral": "referral",
        },
        "back_to_account_button": "Назад к аккаунту",
        "back_to_account_list_button": "Назад к списку аккаунтов",
        "next_button": "След. >>",
        "prev_button": "<< Пред.",
        "back_to_payouts": "К монетам",
        "back_to_income": "К монетам",
        "back_to_workers": "К монетам",
        "back_to_notif": "К монетам",
        "delete_account_descr": "Вы хотите удалить {account_name}\nПосле этого действия все настройки удалятся и вам перестанут приходить оповещения\n\nПодтвердите нажав кнопку внизу",
        "account_deleted_descr": "Аккаунт успешно удален",
        "notification_change_descr": "Настройки уведомлений аккаунта {account_name}\nСейчас уведомления о смене статуса воркеров {setting}",
        "setting_notification": {
            1: "Включены",
            0: "Выключены",
        },
        "setting_notification_set": {
            0: "Выключить",
            1: "Включить",
        },
        "yes": "Да",
        "no": "Нет",
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
