import typing

from aiogram import types
from bot.common.keyboard_fabrics import conv_cb, flow_cb
from bot.common.lang import LangHolder
from config import INTERCOM_TOKEN, PER_PAGE_CONVERSATIONS
from database.user_repo import UserRepository
from third_party.intercom_client.client import IntercomClient
from utils.get_or_create_intercom_contact import get_intercom_contact
from datetime import datetime


async def flow_page(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: LangHolder,
):
    conversation_id = int(callback_data['conv_id'])
    page = int(callback_data['id'])
    
    async with IntercomClient(INTERCOM_TOKEN) as intercom:
        intercom_conversation = await intercom.retrieve_conversation(conversation_id)

        comments = [intercom_conversation['source']] + [i for i in intercom_conversation['conversation_parts']['conversation_parts'] if i['part_type'] in ('comment', 'assignment',)]
        last_message = sorted(comments, key=lambda x: x.get('created_at', 0), reverse=True)[page]

        keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
        keyboard_markup.row(
            types.InlineKeyboardButton(
                _['feedback_reply_button'],
                callback_data=conv_cb.new(
                    id=conversation_id, action="reply",
                ),
            ),
        )
        buttons = []

        if (last_message['type'] != 'conversation'):
            buttons.append(
                types.InlineKeyboardButton(
                    _["prev_button"],
                    callback_data=flow_cb.new(
                        id=page + 1, action="page", conv_id=conversation_id,
                    ),
                )
            )

        buttons.append(
            types.InlineKeyboardButton(
                f"{len(comments) - page}/{len(comments)}",
                callback_data="do_nothing"
            )
        )

        if (page >= 1):
            buttons.append(
                types.InlineKeyboardButton(
                    _["next_button"],
                    callback_data=flow_cb.new(
                        id=page - 1, action="page", conv_id=conversation_id,
                    ),
                )
            )


        keyboard_markup.row(
            *buttons
        )
        
        attachments_text = ''
        if (last_message['attachments']):
            attachments_text = '\n'.join([_['conversation_description_attachments'].format(link=f"<a href=\"{i['url']}\">{i['name']}</a>") for i in last_message['attachments']])

        await query.message.edit_text(_['conversation_description'].format(
            from_who=_['support'] if last_message['author']['type'] == 'admin' else _['not_support'],
            text=last_message['body'],
            time=datetime.fromtimestamp(last_message.get('updated_at', intercom_conversation['created_at'])).strftime("%d/%m/%Y %H:%M:%S"),
            attachments=attachments_text,
        ), reply_markup=keyboard_markup, disable_web_page_preview=True,)
        
        await query.answer()