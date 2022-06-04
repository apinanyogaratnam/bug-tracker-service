from flask import request
from flask_restful import Resource

from controllers.response import Response
from controllers.utility import BaseAPI


class UsersController(Resource):
    def __init__(self: 'UsersController', base_api: BaseAPI) -> None:
        self.base_api = base_api

    def get(self: 'UsersController', email: str = None) -> Response:
        if email:
            user = self.get_user(email)

            if user: return Response(response_data=user, status_code=200)

            return Response(response_data={}, status_code=404)

        users = self.get_users()
        return Response(response_data=users, status_code=200)

    def get_user(self: 'UsersController', email: str) -> dict:
        query_user: str = f'''
            SELECT
                internal_user_id,
                external_user_id,
                username,
                email,
                project_ids,
                EXTRACT(EPOCH FROM created_at) AS created_at
            FROM users
            WHERE email = '{email}';
        '''

        user: dict = self.base_api.create_pandas_table(query_user).to_dict(orient='records')

        return user[0] if user else None

    def get_users(self: 'UsersController') -> list:
        return list()

    def post(self: 'UsersController') -> Response:
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
