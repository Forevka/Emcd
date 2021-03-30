from database.question_repo import QuestionRepository
from aiogram import types
from database.user_repo import UserRepository
from utils.keyboard_fabrics import question_answer_cb
from math import ceil

PER_PAGE = 4

async def cmd_faq(message: types.Message, user: UserRepository, _: dict):
    page = 1
    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    me = await user.get_user(message.from_user.id)

    q_repo = QuestionRepository(user.connection)

    questions = await q_repo.get_question_answers_enabled_by_lang_id(me.lang_id)
    for n, q in enumerate(questions[(page - 1) * PER_PAGE: page * PER_PAGE]):
        inline_keyboard_markup.row(
            types.InlineKeyboardButton(
                    f"#{(page - 1) * PER_PAGE + n + 1} {q.question_text}",
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
            
    buttons.append(
        types.InlineKeyboardButton(
            f"{page}/{ceil(len(questions) / PER_PAGE)}",
            callback_data="do_nothing"
        ),
    )

    if (len(questions) > page * PER_PAGE):
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
