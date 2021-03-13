from database.models.question_answer_translation import QuestionAnswerTranslate
import typing
from typing import List

from asyncpg.connection import Connection

class QuestionRepository:
    def __init__(self, con: Connection):
        self.connection = con

    async def add_faq_answer(self, lang_id: int, question_translation: str, answer_translation: str):
        sql = """
        insert into "question" (status)
        values (1)
        returning "id"
        """

        q_id = (await self.connection.fetchrow(sql,))['id']

        sql = """
        insert into question_translation(question_id, lang_id, translation)
        values ($1, $2, $3)
        """

        await self.connection.execute(sql, q_id, lang_id, question_translation,)

        
        sql = """
        insert into question_answer_translation(question_id, lang_id, translation)
        values ($1, $2, $3)
        """

        await self.connection.execute(sql, q_id, lang_id, answer_translation,)

        return q_id

    async def update_question_by_lang_id_question_id(self, lang_id: int, question_id: int, question_translation: str, answer_translation: str):
        sql = """
        update question_translate
        set translation = $1
        where lang_id = $2 and question_id = $3
        """

        await self.connection.execute(sql, question_translation, lang_id, question_id,)

        sql = """
        update question_answer_translate
        set translation = $1
        where lang_id = $2 and question_id = $3
        """

        await self.connection.execute(sql, answer_translation, lang_id, question_id,)

    async def get_question_answers_by_lang_id(self, lang_id: int) -> typing.List[QuestionAnswerTranslate]:
        sql = f"{QuestionAnswerTranslate.__select__}  where qt.lang_id = $1"

        return [QuestionAnswerTranslate(**acc) for acc in await self.connection.fetch(sql, lang_id,)]

    
    async def get_question_answers_by_lang_id_question_id(self, lang_id: int, question_id: int) -> QuestionAnswerTranslate:
        sql = f"{QuestionAnswerTranslate.__select__}  where qt.lang_id = $1 and q.\"id\" = $2"

        res = await self.connection.fetchrow(sql, lang_id, question_id)
        if (res):
            return QuestionAnswerTranslate(**res)