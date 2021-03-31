import typing

from aiogram import types
from babel.numbers import format_currency
from config import FALLBACK_CURRENCY, SELECT_COIN_CB
from database.user_repo import UserRepository
from enums.coin import Coin
from loguru import logger
from third_party.coincap_client.client import CoinCapClient
from third_party.coincap_client.models.exchange_coin_to_currency import \
    ExchangeCoinToCurrency
from third_party.emcd_client.client import EmcdClient
from utils.common_replies import reply_to_account_not_found
from utils.keyboard_fabrics import menu_cb, statistic_cb
from utils.lang import LangHolder
from utils.utils import grouper

PER_PAGE = 5

async def statistic_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
):
    account_id = callback_data["id"]

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)
    
    if (account is None):
        return await reply_to_account_not_found(query.message, _)
        
    btn_list = []

    for coin in await user.get_account_coins(query.from_user.id, account_id):
        if coin.is_active:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name}",
                    callback_data=statistic_cb.new(
                        id=account_id, type=coin.coin_id,
                    ),
                ),
            )

    for i in grouper(2, btn_list):
        keyboard_markup.add(*i)


    keyboard_markup.add(
        types.InlineKeyboardButton(
            _['back_to_account_button'],
            callback_data=menu_cb.new(id=account.account_id, type="account", action='open'),
        ),
    )
    
    await query.message.edit_text(
        _["statistic_choose_coin"],
        reply_markup=keyboard_markup,
    )

# take second element for sort
def take_update_timestamp(elem: ExchangeCoinToCurrency):
    '''
        COIN cap have bug
        fields updated and trades_count24_hr are swapped
        lol
    '''
    return elem.trades_count24_hr #WTF

async def statistic_info_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
):
    account_id = callback_data["id"]
    coin_id = callback_data['type']

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)

    if (account is None):
        return await reply_to_account_not_found(query.message, _)

    account_coin = next((i for i in await user.get_account_coins(query.from_user.id, account_id) if i.coin_id == coin_id), None,)

    buttons = []
    
    coins = [coin for coin in await user.get_account_coins(query.from_user.id, account_id) if coin.is_active]

    if (len(coins) == 1): #in case if enabled only one coin we treat them as default
        buttons.append(
            types.InlineKeyboardButton(
                _["cabinet"],
                callback_data=menu_cb.new(
                    id=account_id, type="account", action="open"
                ),
            ),
        )
    else:
        buttons.append(
            types.InlineKeyboardButton(
                _["back_to_statistic"],
                callback_data=statistic_cb.new(
                    id=account_id, type=SELECT_COIN_CB,
                ),
            ),
        )

    keyboard_markup.row(*buttons)

    account_api = None
    currency_list = None

    user_currency = await user.get_user_currency(query.from_user.id)

    async with EmcdClient(account_id) as client:
        account_api = await client.get_info()

    if (account_api is None):
        await query.answer()
        logger.warning('account_api is none')
        return

    is_fallback = False

    async with CoinCapClient() as client:
        c_id = coin_id
        if (c_id == 'bchn'):
            c_id = 'bch'

        currency_list = await client.get_info_for_exchange(c_id, user_currency.currency_code)        

        if (len(currency_list.data) == 0):
            currency_list = await client.get_info_for_exchange(c_id, FALLBACK_CURRENCY)
            is_fallback = True


    curr = sorted(currency_list.data, key=take_update_timestamp)[0]

    coin_info = account_api.get_coins()[coin_id]

    message_text = ""

    if (is_fallback):
        message_text = _['currency_not_found'].format(
            currency_code=user_currency.currency_code,
            fallback_currency_code=FALLBACK_CURRENCY,
        ) + '\n'

    message_text += _['statistic_descr'].format(
        account_name=account.username,
        address=account_coin.address,

        current_balance=format(coin_info.balance, '.8f'),
        current_balance_dol=format_currency(round(coin_info.balance * curr.price_usd, 4), '', locale="en_US"),
        current_balance_sec=format_currency(round(coin_info.balance * curr.price_quote, 4), '', locale="en_US"),
        current_balance_sec_symbol=curr.quote_symbol,

        total_paid=format(coin_info.total_paid, '.8f'),
        total_paid_dol=format_currency(round(coin_info.total_paid * curr.price_usd, 4), '', locale="en_US"),
        total_paid_sec=format_currency(round(coin_info.total_paid * curr.price_quote, 4), '', locale="en_US"),
        total_paid_sec_symbol=curr.quote_symbol,

        currency_dol=format_currency(round(curr.price_usd, 2), '', locale="en_US"),
        currency_sec=format_currency(round(curr.price_quote, 2), '', locale="en_US"),
        currency_sec_symbol=curr.quote_symbol,
    )

    await query.message.edit_text(
        message_text,
        reply_markup=keyboard_markup,
    )
