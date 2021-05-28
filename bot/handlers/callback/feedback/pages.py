import typing

from aiogram import types
from bot.common.keyboard_fabrics import conv_cb
from bot.common.lang import LangHolder
from config import INTERCOM_TOKEN, PER_PAGE_CONVERSATIONS
from database.user_repo import UserRepository
from third_party.intercom_client.client import IntercomClient
from utils.get_or_create_intercom_contact import get_intercom_contact


async def conversation_pages(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
):
    page = int(callback_data['id'])

    async with IntercomClient(INTERCOM_TOKEN) as intercom:

        intercom_user = await get_intercom_contact(query.from_user)

        conversations = await intercom.find_conversations_for_user(
            intercom_user["id"]
        )

        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)

        if conversations["total_count"] > 0:
            current_conv_page = conversations["conversations"][(page - 1) * PER_PAGE_CONVERSATIONS: page * PER_PAGE_CONVERSATIONS]

            for conv in current_conv_page:
                keyboard_markup.add(
                    types.InlineKeyboardButton(
                        f'#{conv["id"]} - ' + (_["feedback_opened"] if conv["open"] else _["feedback_closed"]),
                        callback_data=conv_cb.new(
                            id=conv["id"], action="open"
                        ),
                    )
                )
                
            buttons = []

            if (page > 1):
                buttons.append(
                    types.InlineKeyboardButton(
                        _["prev_button"],
                        callback_data=conv_cb.new(
                            id=page - 1, action="page",
                        ),
                    ),
                )

            buttons.append(
                types.InlineKeyboardButton(
                    _['new_feedback'],
                    callback_data=conv_cb.new(
                        id="_", action="new"
                    ),
                )
            )
            
            if (len(current_conv_page) >= 1 * PER_PAGE_CONVERSATIONS):
                buttons.append(
                    types.InlineKeyboardButton(
                        _["next_button"],
                        callback_data=conv_cb.new(
                            id=page + 1, action="page",
                        ),
                    ),
                )

            keyboard_markup.row(*buttons)

            await query.message.edit_text(
                _["feedback_menu_has_items"].format(
                    open=sum(
                        (1 for i in conversations["conversations"] if i["open"]), 0
                    ),
                    closed=sum(
                        (1 for i in conversations["conversations"] if not i["open"]), 0
                    )
                ),
                reply_markup=keyboard_markup,
            )
            return

        keyboard_markup.row(
            types.InlineKeyboardButton(
                _['new_feedback_button'],
                callback_data=conv_cb.new(
                    id="_", action="new"
                ),
            )
        )

        await query.message.edit_text(
            _["feedback_menu_no_items"],
            reply_markup=keyboard_markup,
        )
