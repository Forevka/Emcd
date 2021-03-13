import json

from database.question_repo import QuestionRepository
from fastapi import Depends, HTTPException, Request
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from webapi.models.question_answer import QuestionAnswer

async def add_question(request: Request, questionAnswer: QuestionAnswer, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    question_repo = QuestionRepository(request.state.connection)
    
    q_id = await question_repo.add_faq_answer(questionAnswer.langId, questionAnswer.questionTranslation, questionAnswer.answerTranslation)

    question = await question_repo.get_question_answers_by_lang_id_question_id(questionAnswer.langId, q_id)

    return {
        'questionId': q_id,
        'langId': question.lang_id,
        'questionTranslation': question.question_text,
        'answerTranslation': question.answer_text,
        'statusId': 1,
    }