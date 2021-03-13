from aiogram import types
from config import DEFAULT_LANG, POEDITOR_ID, POEDITOR_TOKEN, DEFAULT_CURRENCY
from database.user_repo import UserRepository
from enums.coin import Coin
from enums.lang import Lang
from keyboard_fabrics import lang_cb
from lang import language_map
from poeditor_client.client import PoeditorClient
from utils.utils import grouper


async def cmd_start(message: types.Message, user: UserRepository, _: dict):
    """
    Conversation's entry point
    """

    await user.create(message.from_user.id, int(DEFAULT_LANG.value))

    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btns_text = (_['cabinet'], _['faq'])
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    keyboard_markup.row(_['setting'])

    await message.answer(_['hello'], reply_markup=keyboard_markup)
    
    btn_list = []
    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    langs = None
    async with PoeditorClient(POEDITOR_TOKEN, POEDITOR_ID,) as client:
        langs = [Lang.ru, Lang.en]
        for lang in langs:
            lang_id = lang.value
            if (lang_id is None):
                continue

            btn_list.append(
                types.InlineKeyboardButton(
                    language_map[lang.name],
                    callback_data=lang_cb.new(
                        id=lang_id,
                    ),
                ),
            )

    for i in grouper(2, btn_list):
        inline_keyboard_markup.row(*i)

    await message.answer(_['choose_lang'], reply_markup=inline_keyboard_markup)
    
    await user.add_notification_setting(message.from_user.id, True)
    
    await user.add_user_coin(message.from_user.id, Coin.Bitcoin.value, True)
    await user.add_user_coin(message.from_user.id, Coin.BitcoinHash.value, False)
    await user.add_user_coin(message.from_user.id, Coin.BitcoinSV.value, False)
    await user.add_user_coin(message.from_user.id, Coin.Ethereum.value, False)
    await user.add_user_coin(message.from_user.id, Coin.EthereumClassic.value, False)
    await user.add_user_coin(message.from_user.id, Coin.Litecoin.value, False)
    await user.add_user_coin(message.from_user.id, Coin.Dash.value, False)

    await user.add_user_currency(message.from_user.id, DEFAULT_CURRENCY)
