import typing

from aiogram import types
from database.user_repo import UserRepository
from keyboard_fabrics import notification_cb

async def notificaion_enable_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    action = callback_data['action']

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    notification_setting = await user.get_notification_setting_for_user(query.from_user.id)

    new_setting_value = not notification_setting.is_enabled
    
    if (action != "_"):
        await user.update_notification_setting(query.from_user.id, new_setting_value)

        notification_setting = await user.get_notification_setting_for_user(query.from_user.id)

    keyboard_markup.row(
        types.InlineKeyboardButton(
            _[f'setting_notification_set_{int(not notification_setting.is_enabled)}'],
            callback_data=notification_cb.new(
                action=new_setting_value
            ),
        ),
    )

    message_text = _['notification_change_descr'].format(
        setting=_[f'setting_notification_{int(notification_setting.is_enabled)}']
    )
    
    await query.message.edit_text(
        message_text,
        reply_markup=keyboard_markup,
    )
