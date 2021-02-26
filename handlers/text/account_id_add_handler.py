from config import Coin
from uuid import UUID

from aiogram import types
from aiogram.dispatcher import FSMContext
from database.user_repo import UserRepository
from emcd_client.client import EmcdClient
from keyboard_fabrics import menu_cb


def validate_uuid4(uuid_string: str):

    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False

    return True

async def account_id_add_handler(message: types.Message, user: UserRepository, _: dict, state: FSMContext):
    account_id = message.text

    await state.finish()

    if (validate_uuid4(account_id)):
        user_account = await user.get_accounts(message.from_user.id)

        exist_account = next((acc for acc in user_account if str(acc.account_id) == account_id), None)

        if (not exist_account):
            async with EmcdClient(account_id) as client:
                account = await client.get_info()

                if (account):
                    await user.add_account(message.from_user.id, UUID(account_id, version=4), account.username)
                    await user.add_notification_setting(message.from_user.id, True)

                    coins_api = account.get_coins()

                    for coin in await user.get_coins(message.from_user.id):
                        c = coins_api[coin.coin_id]
                        await user.add_account_coin(message.from_user.id, UUID(account_id, version=4), coin.coin_id, c, coin.is_enabled)

                    await message.answer(_['account_added'].format(account_name=account.username))

                    return
        else:
            await message.answer(_['account_id_already_registered'].format(account_name=exist_account.username))

            return

    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    
    keyboard_markup.add(
        types.InlineKeyboardButton(
            _['again_button'],
            callback_data=menu_cb.new(id='_', type="account", action='new'),
        )
    )

    await message.answer(_['account_id_invalid'], reply_markup=keyboard_markup)
