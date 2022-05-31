from flask import request
from flask_restful import Resource

from controllers.response import Response
from controllers.utility import BaseAPI


class UsersController(Resource):
    def __init__(self: 'Users', base_api: BaseAPI) -> None:
        self.base_api = base_api

    def get(self: 'Users') -> Response:
        return Response(response_data={}, status_code=200)

    def get_user(self: 'Users', email: str) -> dict:
        return {
            'email': email,
            'username': 'username',
            'project_ids': [1, 2, 3]
        }

    def post(self: 'Users') -> Response:
        body: dict | list = request.get_json()

        is_valid_body: bool = True

        if not is_valid_body(body):
            return Response(response_data={}, status_code=400)

        email: str = body.get('email')
        username: str = body.get('username')
        

        user = self.get_user(email)

        if user:
            return Response(response_data={}, status_code=409)

        return Response(response_data={}, status_code=201)
