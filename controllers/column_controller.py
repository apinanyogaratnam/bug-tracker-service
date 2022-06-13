from flask_restful import Resource
from flask import request

from controllers.response import Response
from controllers.utility import BaseAPI
from models import Column


class ColumnController(Resource, Column):
    def __init__(self: 'ColumnController', base_api: BaseAPI) -> None:
        self.base_api = base_api

    def get(self: 'ColumnController') -> Response:
        project_id: int = request.args.get('project_id', type=int, default=None)

        if project_id is None:
            return Response(response_data={}, error='Expected parameter: project_id.', status_code=400)

        columns: list = self.get_columns(project_id)

        if columns is None:
            return Response(response_data={}, error='Not Found', status_code=404)

        return Response(response_data=columns, status_code=200)

    def get_columns(self: 'ColumnController', project_id: int) -> list | None:
        query_user: str = f'''
            SELECT
                column_id,
                project_id,
                raw_columns,
                EXTRACT(EPOCH FROM created_at) AS created_at
            FROM columns
            WHERE project_id = '{project_id}';
        '''

        queried_columns: list = self.base_api.create_pandas_table(query_user).to_dict(orient='records')

        columns: list = []
        for column in queried_columns:
            columns.append(Column(**column).jsonify())
        return columns

    # def post(self: 'ColumnController') -> Response:
    #     body: dict | list = request.get_json()

    #     try:
    #         user_id, name, description = self.validate_body(body)
    #     except ValueError as error:
    #         return Response(response_data={}, error=str(error), status_code=400)

    #     super().__init__(user_id, administrator_id=user_id, co_administrator_ids=[], member_ids=[], name=name, description=description)
    #     self.create()
    #     projects: list = self.get_projects(user_id)

    #     return Response(response_data=projects, status_code=201)

    # def validate_body(self: 'ColumnController', body: dict) -> Tuple[str, str, str]:
    #     user_id, name, description = body.get('user_id'), body.get('name'), body.get('description')

    #     if not user_id or not name or not description:
    #         raise ValueError('Missing required fields in body. Required fields: user_id, name, description')

    #     return user_id, name, description
