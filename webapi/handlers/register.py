from webapi.handlers.conversations.response import response
from webapi.handlers.auth.me import me
from fastapi import FastAPI
from fastapi_jwt_auth.exceptions import AuthJWTException
from webapi.handlers.auth.exception import exception_handler
from webapi.handlers.lang.lang_list import lang_list
from webapi.handlers.auth.token import login
from webapi.handlers.question.add import add_question
from webapi.handlers.question.change import change_question
from webapi.handlers.question.get import get_question
from webapi.handlers.question.question_list import get_question_list
from webapi.handlers.question.delete import delete_question


def register(app: FastAPI):
    app.add_exception_handler(AuthJWTException, exception_handler)

    app.add_api_route(
        '/question/{lang_id}/{question_id}',
        delete_question,
        tags=['Question'],
        methods=['DELETE'],
    )
    app.add_api_route(
        '/question/{lang_id}',
        get_question_list,
        tags=['Question'],
        methods=['GET'],
    )
    app.add_api_route(
        '/question/{lang_id}/{question_id}',
        get_question,
        tags=['Question'],
        methods=['GET'],
    )
    app.add_api_route(
        '/question',
        add_question,
        tags=['Question'],
        methods=['POST'],
    )
    app.add_api_route(
        '/question',
        change_question,
        tags=['Question'],
        methods=['PATCH'],
    )


    app.add_api_route(
        '/lang/list',
        lang_list,
        tags=['Lang'],
        methods=['GET'],
    )

    app.add_api_route(
        '/auth/token',
        login,
        tags=['Auth'],
        methods=['POST'],
    )

    app.add_api_route(
        '/auth/me',
        me,
        tags=['Auth'],
        methods=['GET'],
    )


    app.add_api_route(
        '/conversation/response',
        response,
        tags=['Conversation'],
        methods=['POST'],
    )