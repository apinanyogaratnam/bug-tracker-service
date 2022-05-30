from flask import request
from flask_restful import Resource

from controllers.response import Response


class Users(Resource):
    def __init__(self: 'Users') -> None:
        pass

    def get(self: 'Users') -> Response:
        return Response(response_data={}, status_code=200)

    def get_user(self: 'Users', email: str) -> dict:
        return {
            'email': email,
            'username': 'username',
            'project_ids': [1, 2, 3]
        }
