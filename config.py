import datetime
import os
from enum import Enum

START_TIME = datetime.datetime.now()

postgres = os.environ.get('CONNECTION_STRING')

TOKEN = os.environ.get('TOKEN')

texts = {
    'ru': {
        'setting_descr': "Здесь вы можете изменить глобальные настройки",
        'setting': "Настройки",
        'lang_changed': "Окей, твой язык теперь русский",
        'choose_lang': "Пожалуйста выбери свой язык",
        'language': "Язык/Language",
        'hello': "Привет, я бот для мониторинга системы ECMD\n\nКнопка 'Кабинет' для работы с аккаунтами\nКнопка 'База данных' если у тебя есть вопроc",
        'cabinet_msg': "У тебя {account_count} подключенных аккаунтов. Здесь ты можешь управлять подключенными аккаунтами",
        'add_account': "Попробуй добавить новые аккаунты при помощи кнопки 'Добавить'\n<code>Здесь будет ссылка с инструкцией где взять апи ключ</code>",
        'cabinet': 'Меню',
        'faq': 'База данных',
        'add_account_btn': 'Добавить аккаунт',
        'add_account_descr': 'Отправь мне токен от своего аккаунта',
        'account_added': "Окей, я добавил этот аккаунт. Он будет называться {account_name}\nАвтоматически подключил такие монеты: {coins_list}\nИзменить их ты сможешь через 'Кабинет'",
        'account_id_invalid': 'Твой апи ключ не валидный или аккаунта с таким ключом не существует, обратись в поддержку или попробуй ещё раз',
        'account_id_already_registered': "Аккаунт с таким апи ключом уже зарегистрирован за вами его имя {account_name}. Проверьте валидность ключа или напишите в поддержку.\nУправление аккаунтом через кнопку 'Кабинет'",
        'again_button': 'Ещё раз',
        'account_cabinet': 'Меню и статистика аккаунта {account_name}\n\nЗдесь ты можешь посмотреть статистику аккаунта',
        'change_coins_button': "Изменить список монет",
        'coin_list_descr': "Список подключенных монет для аккаунта {account_name}:",
        'coin_disabled': "Монета выключена ❌",
        'coin_enabled': "Монета включена ✅",
        'finance_button': "Финансы",
        'statistic_button': "Статистика",
        'workers_stat_button': "Устройства(Воркеры)",
        'income_stat_button': "Начисления",
        'payouts_stat_button': "Выплаты",
        'statistic_choose_coin': "Выберите по какой монете вы хотите посмотреть статистику\nИзменить список монет можно в меню аккаунта",
        'payouts_choose_coin': "Выберите по какой монете вы хотите посмотреть выплаты\nИзменить список монет можно в меню аккаунта",
        'income_choose_coin': "Выберите по какой монете вы хотите посмотреть начисления\nИзменить список монет можно в меню аккаунта",
        'worker_choose_coin': "Выберите по какой монете вы хотите посмотреть статистику воркеров\nИзменить список монет можно в меню аккаунта",
        'notification_choose_coin': "Выберите по какой монете вы хотите изменить настройки уведомлений\nИзменить список монет можно в меню аккаунта",
        'hashrate': "Хешрейт",
        'current': "Текущий",
        '1_hour': "1 час",
        '24_hour': "24 часа",
        'worker_info_descr': '''Общая статистика аккаунта
- - - - - - - - - - - - - - - - - - - - - - - 
⏺ Текущий: {hashrate}
⏺ 1 час: {hashrate1h}
⏺ 24 часа: {hashrate24h}
- - - - - - - - - - - - - - - - - - - - - - - 


Воркеры
- - - - - - - - - - - - - - - - - - - - - - - 
⏺ Всего: {total}
⏺ Активных: {active}
⏺ Неактивные: {inactive}
⏺ Мертвых: {dead}
- - - - - - - - - - - - - - - - - - - - - - - 
{description}
''',#"Статистика по воркерам аккаунта {account_name}\nВсего: {total}\nАктивных: {active}\nМёртвых: {dead}\nНеактивных: {inactive}\n{description}",
        'statistic_descr': '''Статистика аккаунта {account_name}
💶 Текущий Баланс: {current_balance} ({current_balance_dol}$)
🕔 Всего выплачено: {total_paid} ({total_paid_dol}$)
📬 Адрес выплаты: {address}
📊 Курс: {course_dol}$ ({course_rub} RUB)
        ''',
        'notifcation_button': "Уведомления",
        'notification_on': "Оповещения вкл. ✅",
        'notification_off': "Оповещения выкл. ❌",
        'delete_account': "Удаление аккаунтов",
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
        "back_to_statistic": "К монетам",
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
        'setting': "Settings",
        'lang_changed': "Ok, your language chagned to english",
        'choose_lang': "Please choose your language from below",
        'language': "Language/Язык",
        'hello': "Hello! I'm monitoring bot for EMCD system\n\nButton 'Account' for work with accounts\nButton 'FAQ' if you have a question",
        'cabinet_msg': "You have {account_count} registered accounts. Here you can manage them",
        'add_account': "Try to register new account with button 'Add'\n<code>Here will be instruction which describe how to obtain api-key</code>",
        'cabinet': 'Menu',
        'faq': 'FAQ',
        'add_account_btn': 'Add account',
        'add_account_descr': 'Please send me token from your account',
        'account_added': "Ok, i've added your account. They will be named {account_name}\nAutomatically detected this coins: {coins_list}\nYou can change them in 'Account' button",
        'account_id_invalid': 'Your api key is invalid. Please check this key or message to support',
        'account_id_already_registered': "You already registered this account, they named as {account_name}. Please check this key for validity or message support.\nAccount management in 'Account' button",
        'again_button': 'Try again',
        'account_cabinet': 'Account management for {account_name}\n\nLinked coins: {coins_list}\n\nHere you can change coin list, enable/disable notification and check account stats',
        'change_coins_button': "Change coin list",
        'coin_list_descr': "List of linked coins to account  {account_name}:",
        'coin_disabled': "Coin are disabled ❌",
        'coin_enabled': "Coin are enabled ✅",
        'workers_stat_button': "Workers",
        'income_stat_button': "Income",
        'payouts_stat_button': "Payouts",
        'payouts_choose_coin': "Choose coin to see payouts\nList of available coins you can change in previous menu",
        'income_choose_coin': "Choose coin to see incomes\nList of available coins you can change in previous menu",
        'worker_choose_coin': "Choose coin to see worker statistic\nList of available coins you can change in previous menu",
        'notification_choose_coin': "Choose coin to see notification setting\nList of available coins you can change in previous menu",
        'worker_info_descr': "Worker statistic for account {account_name}\nTotal: {total}\nActive: {active}\nDead: {dead}\nInactive: {inactive}\n{description}",
        'notifcation_button': "Notifications",
        'notification_on': "Enable notifications ✅",
        'notification_off': "Disable notifications ❌",
        'delete_account': "Delete account",
        'worker_changed_status_descr': "{worker_name} - ({previous_status}) to ({new_status})",
        'worker_changed_status_body': "Workers changed their status {account_name}\n\n{description}",
        'status': {
            -1: "Dead",
            0: "Inactive",
            1: "Active",
            2: "Non stable",
        },
        'income_names': {
            "donation": "donation",
            "fpps": "fpps",
            "referral": "referral",
        },
        "back_to_account_button": "Back to account",
        "back_to_account_list_button": "Back to account list",
        "next_button": "Next. >>",
        "prev_button": "<< Prev.",
        "back_to_payouts": "To coins",
        "back_to_income": "To coins",
        "back_to_workers": "To coins",
        "back_to_notif": "To coins",
        "delete_account_descr": "You wan't to delete {account_name}\nAfter this action bot will erase all settings related to this account\n\nIf you agree please tap on button below",
        "account_deleted_descr": "Account succesfully deleted",
        "notification_change_descr": "Notification setting on account {account_name}\nNotification are: {setting}",
        "setting_notification": {
            1: "Enabled",
            0: "Disabled",
        },
        "setting_notification_set": {
            0: "Disable",
            1: "Enable",
        },
        "yes": "Yes",
        "no": "No",
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
