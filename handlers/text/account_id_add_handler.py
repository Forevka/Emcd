from emcd_client.client import EmcdClient
from database.user_repo import UserRepository
from aiogram import types
from aiogram.dispatcher import FSMContext
from uuid import UUID

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
        async with EmcdClient(account_id) as client:
            account = await client.get_info()

            if (account):
                await message.answer(_['account_added'].format(account_name=account.username))

                return

    
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    
    keyboard_markup.add(
        types.InlineKeyboardButton(
            _['again_button'],
            callback_data=menu_cb.new(id='_', type="account", action='new'),
        )
    )

    await message.answer(_['account_id_invalid'], reply_markup=keyboard_markup)