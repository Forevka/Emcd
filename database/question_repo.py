from database.models.question_answer_translation import QuestionAnswerTranslate
import typing
from typing import List

from asyncpg.connection import Connection

class QuestionRepository:
    def __init__(self, con: Connection):
        self.connection = con

    async def get_question_answers_by_lang_id(self, lang_id: int) -> typing.List[QuestionAnswerTranslate]:
        sql = f"{QuestionAnswerTranslate.__select__}  where qt.lang_id = $1"

        return [QuestionAnswerTranslate(**acc) for acc in await self.connection.fetch(sql, lang_id,)]

    
    async def get_question_answers_by_lang_id_question_id(self, lang_id: int, question_id: int) -> QuestionAnswerTranslate:
        sql = f"{QuestionAnswerTranslate.__select__}  where qt.lang_id = $1 and q.\"id\" = $2"

        res = await self.connection.fetchrow(sql, lang_id, question_id)
        if (res):
            return QuestionAnswerTranslate(**res)