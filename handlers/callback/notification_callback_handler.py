import typing

from aiogram import types
from config import Coin
from database.user_repo import UserRepository
from emcd_client.client import EmcdClient
from keyboard_fabrics import income_cb, menu_cb, notification_cb
from utils import grouper

PER_PAGE = 5

async def notification_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)
    
    btn_list = []

    for coin in await user.get_account_coins(query.from_user.id, account_id):
        if coin.is_active:
            btn_list.append(
                types.InlineKeyboardButton(
                    f"{Coin(coin.coin_id).name}",
                    callback_data=notification_cb.new(
                        id=account_id, type=coin.coin_id, action='_'
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
        _["notification_choose_coin"],
        reply_markup=keyboard_markup,
    )


async def notificaion_enable_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    account_id = callback_data["id"]
    coin_id = callback_data['type']
    action = callback_data['action']

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    
    account = next((acc for acc in await user.get_accounts(query.from_user.id) if str(acc.account_id) == account_id), None,)

    account_coin = next((i for i in await user.get_account_coins(query.from_user.id, account_id) if i.coin_id == coin_id), None,)

    notification_setting = await user.get_notification_setting_for_account(account_coin.id)

    new_setting_value = not notification_setting.is_enabled

    
    if (action != "_"):
        await user.update_notification_setting_for_account(account_coin.id, new_setting_value)

        notification_setting = await user.get_notification_setting_for_account(account_coin.id)

    keyboard_markup.row(
        types.InlineKeyboardButton(
            _['setting_notification_set'][int(not notification_setting.is_enabled)],
            callback_data=notification_cb.new(
                id=account_id, type=coin_id, action=new_setting_value
            ),
        ),
    )

    message_text = _['notification_change_descr'].format(
        account_name=account.username,
        setting=_['setting_notification'][notification_setting.is_enabled]
    )


    keyboard_markup.row(
        types.InlineKeyboardButton(
            _["back_to_notif"],
            callback_data=notification_cb.new(
                id=account_id, action="_", type='s_coin',
            ),
        ),
    )
    
    await query.message.edit_text(
        message_text,
        reply_markup=keyboard_markup,
    )
