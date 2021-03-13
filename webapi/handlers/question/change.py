import json

from database.question_repo import QuestionRepository
from fastapi import Depends, HTTPException, Request
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from webapi.models.question_answer import QuestionAnswer

async def change_question(request: Request, questionAnswer: QuestionAnswer, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    question_repo = QuestionRepository(request.state.connection)
    
    await question_repo.update_question_by_lang_id_question_id(questionAnswer.lang_id, questionAnswer.questionId, questionAnswer.questionTranslation, questionAnswer.answerTranslation)

    question = await question_repo.get_question_answers_by_lang_id_question_id(questionAnswer.langId, questionAnswer.questionId)

    return {
        'questionId': q_id,
        'langId': question.lang_id,
        'questionTranslation': question.question_text,
        'answerTranslation': question.answer_text,
        'statusId': 1,
    }