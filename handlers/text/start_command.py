from aiogram import types
from config import Coin, DEFAULT_LANG, Lang
from database.user_repo import UserRepository
from keyboard_fabrics import lang_cb


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
    
    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    inline_keyboard_markup.row(
        types.InlineKeyboardButton(
            "Русский",
            callback_data=lang_cb.new(
                id=Lang.ru.value,
            ),
        ),
    )
    
    inline_keyboard_markup.row(
        types.InlineKeyboardButton(
            "English",
            callback_data=lang_cb.new(
                id=Lang.en.value,
            ),
        ),
    )

    await message.answer(_['choose_lang'], reply_markup=inline_keyboard_markup)
    
    await user.add_user_coin(message.from_user.id, Coin.Bitcoin.value, True)
    await user.add_user_coin(message.from_user.id, Coin.BitcoinHash.value, False)
    await user.add_user_coin(message.from_user.id, Coin.BitcoinSV.value, False)
    await user.add_user_coin(message.from_user.id, Coin.Ethereum.value, False)
    await user.add_user_coin(message.from_user.id, Coin.EthereumClassic.value, False)
    await user.add_user_coin(message.from_user.id, Coin.Litecoin.value, False)
    await user.add_user_coin(message.from_user.id, Coin.Dash.value, False)
