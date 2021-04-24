from bot.handlers.text.base_command_handler import BaseCommandHandler
from math import ceil

from aiogram import types
from bot.common.keyboard_fabrics import question_answer_cb
from config import PER_PAGE_FAQ
from database.question_repo import QuestionRepository
from database.user_repo import UserRepository


class CmdFaq(BaseCommandHandler):
    async def handle(self, message: types.Message, user: UserRepository, _: dict):
        page = 1
        inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        me = await user.get_user(message.from_user.id)

        q_repo = QuestionRepository(user.connection)

        questions = await q_repo.get_question_answers_enabled_by_lang_id(me.lang_id)
        for n, q in enumerate(questions[(page - 1) * PER_PAGE_FAQ: page * PER_PAGE_FAQ]):
            inline_keyboard_markup.row(
                types.InlineKeyboardButton(
                        f"#{(page - 1) * PER_PAGE_FAQ + n + 1} {q.question_text}",
                        callback_data=question_answer_cb.new(
                            id=q.id, page=page, action="open",
                        ),
                    ),
            )
        
        buttons = []
        if (page > 1):
            buttons.append(
                types.InlineKeyboardButton(
                    _["prev_button"],
                    callback_data=question_answer_cb.new(
                        id="_", page=page - 1, action="page",
                    ),
                ),
            )
        
        if (questions):
            buttons.append(
                types.InlineKeyboardButton(
                    f"{page}/{ceil(len(questions) / PER_PAGE_FAQ)}",
                    callback_data="do_nothing"
                ),
            )

        if (len(questions) > page * PER_PAGE_FAQ):
            buttons.append(
                types.InlineKeyboardButton(
                    _["next_button"],
                    callback_data=question_answer_cb.new(
                        id="_", page=page + 1, action="page",
                    ),
                ),
            )

        inline_keyboard_markup.row(*buttons)
        
        await message.answer(_['faq_msg_descr'], reply_markup=inline_keyboard_markup)

    __call__ = handle