from typing import Tuple

from flask import request
from flask_restful import Resource

from controllers.response import Response
from controllers.utility import BaseAPI
from models import User


class UsersController(Resource, User):
    def __init__(self: 'UsersController', base_api: BaseAPI) -> None:
        self.base_api = base_api

    def get(self: 'UsersController', email: str = None) -> Response:
        if email:
            cache_key: str = f'get_user_{email}'
            cache_value: object = self.base_api.get_cache(cache_key)
            if cache_value: return Response(response_data=cache_value, status_code=200)

            user = self.get_user(email)

            if user:
                self.base_api.set_cache(cache_key, user, 3600)
                return Response(response_data=user, status_code=200)

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
                EXTRACT(EPOCH FROM created_at) AS created_at
            FROM users
            WHERE email = '{email}';
        '''

        user: list = self.base_api.create_pandas_table(query_user).to_dict(orient='records')

        return user[0] if user else None

    def get_users(self: 'UsersController') -> list:
        query_user: str = '''
            SELECT
                internal_user_id,
                external_user_id,
                username,
                email,
                EXTRACT(EPOCH FROM created_at) AS created_at
            FROM users;
        '''

        users: list = self.base_api.create_pandas_table(query_user).to_dict(orient='records')

        return users

    def post(self: 'UsersController') -> Response:
        body: dict | list = request.get_json()

        try:
            email, username, external_user_id = self.validate_body(body)
        except ValueError as error:
            return Response(response_data={}, error=str(error), status_code=400)

        user = self.get_user(email)

        if user:
            return Response(response_data={}, error='User already exists', status_code=409)

        super().__init__(external_user_id, username, email)
        user: dict = self.create().jsonify()

        return Response(response_data=user, status_code=201)

    def validate_body(self: 'UsersController', body: dict) -> Tuple[str, str, str]:
        email, username, external_user_id = body.get('email'), body.get('username'), body.get('external_user_id')

        if not email or not username or not external_user_id:
            raise ValueError('Missing required fields in body. Required Fields: email, username, external_user_id')

        return email, username, external_user_id
