from typing import List, Tuple
from uuid import uuid4

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

        columns: List[Column] = self.get_columns(project_id)
        serialized_columns: List[dict] = self.jsonify_columns(columns)

        if columns is None:
            return Response(response_data={}, error='Not Found', status_code=404)

        return Response(response_data=serialized_columns, status_code=200)

    def get_columns(self: 'ColumnController', project_id: int) -> List[Column]:
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

        columns: list = list(map(lambda column: Column(**column), queried_columns))
        return columns

    def jsonify_columns(self: 'ColumnController', columns: List[Column]) -> List[dict]:
        return [column.jsonify() for column in columns]

    def post(self: 'ColumnController') -> Response:
        body: dict | list = request.get_json()

        try:
            project_id, raw_columns = self.validate_body(body)
        except ValueError as error:
            return Response(response_data={}, error=str(error), status_code=400)

        super().__init__(project_id, raw_columns)
        self.create()
        columns: List[Column] = self.get_columns(project_id)
        serialized_columns: List[dict] = self.jsonify_columns(columns)

        return Response(response_data=serialized_columns, status_code=201)

    # TODO: implement this and delete method
    def put(self: 'ColumnController', column_id: int) -> Response:
        body: dict | list = request.get_json()

        column_name = self.validate_body(body)

        column: Column = self.get_column(column_id)

        raw_columns: dict = column.raw_columns
        new_column_id: int = column.get_last_column_id() + 1
        raw_columns[new_column_id] = {'name': column_name, 'items': []}

        # TODO: column.update(raw_columns)

        return Response(response_data={}, error='Not Implemented', status_code=501)

    def validate_body(self: 'ColumnController', body: dict) -> Tuple[str, str]:
        column_name: str = body.get('column_name')

        if not column_name:
            raise ValueError('Missing required fields in body. Required fields: column_name.')

        return column_name

    def get_column(self: 'ColumnController', column_id: int) -> Column:
        query_user: str = f'''
            SELECT
                column_id,
                project_id,
                raw_columns,
                EXTRACT(EPOCH FROM created_at) AS created_at
            FROM columns
            WHERE column_id = '{column_id}'
            LIMIT 1;
        '''

        queried_columns: list = self.base_api.create_pandas_table(query_user).to_dict(orient='records')

        if len(queried_columns) == 0:
            raise ValueError('Not Found')

        return Column(**queried_columns[0])
