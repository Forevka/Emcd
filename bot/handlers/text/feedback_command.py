from aiogram import types
from aiogram.types.chat import ChatActions
from bot.common.keyboard_fabrics import conv_cb
from bot.handlers.text.base_command_handler import BaseCommandHandler
from config import INTERCOM_TOKEN, PER_PAGE_CONVERSATIONS
from database.user_repo import UserRepository
from third_party.intercom_client.client import IntercomClient
from utils.get_or_create_intercom_contact import get_intercom_contact


class CmdFeedback(BaseCommandHandler):
    async def handle(self, message: types.Message, user: UserRepository, _: dict):
        await message.bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
        async with IntercomClient(INTERCOM_TOKEN) as intercom:

            intercom_user = await get_intercom_contact(message.from_user)

            conversations = await intercom.find_conversations_for_user(
                intercom_user["id"]
            )

            keyboard_markup = types.InlineKeyboardMarkup(row_width=1)

            if conversations["total_count"] > 0:
                for conv in conversations["conversations"][(1 - 1) * PER_PAGE_CONVERSATIONS: 1 * PER_PAGE_CONVERSATIONS]:
                    keyboard_markup.add(
                        types.InlineKeyboardButton(
                            f'#{conv["id"]} - ' + (_["feedback_opened"] if conv["open"] else _["feedback_closed"]),
                            callback_data=conv_cb.new(
                                id=conv["id"], action="open"
                            ),
                        )
                    )
                    
                buttons = []

                buttons.append(
                    types.InlineKeyboardButton(
                        _['new_feedback_button'],
                        callback_data=conv_cb.new(
                            id="_", action="new"
                        ),
                    )
                )
                
                if (len(conversations["conversations"]) > 1 * PER_PAGE_CONVERSATIONS):
                    buttons.append(
                        types.InlineKeyboardButton(
                            _["next_button"],
                            callback_data=conv_cb.new(
                                id=2, action="page",
                            ),
                        ),
                    )



                keyboard_markup.row(*buttons)

                await message.answer(
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

            await message.answer(
                _["feedback_menu_no_items"],
                reply_markup=keyboard_markup,
            )

    __call__ = handle
