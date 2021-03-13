import json

from database.question_repo import QuestionRepository
from fastapi import Depends, HTTPException, Request
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from webapi.models.question_answer import QuestionAnswer

async def get_question_list(request: Request, lang_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    question_repo = QuestionRepository(request.state.connection)
    
    questions = await question_repo.get_question_answers_by_lang_id(lang_id,)

    return [{
        'questionId': question.id,
        'langId': question.lang_id,
        'questionTranslation': question.question_text,
        'answerTranslation': question.answer_text,
        'statusId': question.status,
    } for question in questions]