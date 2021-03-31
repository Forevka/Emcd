import typing
from math import ceil

from aiogram import types
from database.question_repo import QuestionRepository
from database.user_repo import UserRepository
from utils.keyboard_fabrics import question_answer_cb

PER_PAGE = 4

async def faq_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    page = int(callback_data['page'])

    inline_keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    me = await user.get_user(query.from_user.id)

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
    
    await query.message.edit_text(
        _["faq_msg_descr"],
        reply_markup=inline_keyboard_markup,
    )


async def faq_info_callback_handler(
    query: types.CallbackQuery,
    callback_data: typing.Dict[str, str],
    user: UserRepository,
    _: dict,
):
    question_id = int(callback_data["id"])
    page = callback_data['page']

    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)

    me = await user.get_user(query.from_user.id)

    q_repo = QuestionRepository(user.connection)

    keyboard_markup.row(
        types.InlineKeyboardButton(
            _["faq_back_to_list"],
            callback_data=question_answer_cb.new(
                id="_", page=page, action="page",
            ),
        ),
    )
    
    question_answer = await q_repo.get_question_answers_by_lang_id_question_id(me.lang_id, question_id)
    
    await query.message.edit_text(
        question_answer.answer_text,
        reply_markup=keyboard_markup,
        disable_web_page_preview=True,
    )
