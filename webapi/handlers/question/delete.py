import json

from database.question_repo import QuestionRepository
from fastapi import Depends, HTTPException, Request
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from webapi.models.question_answer import QuestionAnswer

async def delete_question(request: Request, lang_id: int, question_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    question_repo = QuestionRepository(request.state.connection)
    
    await question_repo.delete(lang_id, question_id)

    question = await question_repo.get_question_answers_by_lang_id_question_id(lang_id, question_id)

    return {}