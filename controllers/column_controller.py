from typing import List, Tuple

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

        columns: list = []
        for column in queried_columns:
            columns.append(Column(**column))
        return columns

    def jsonify_columns(self: 'ColumnController', columns: List[Column]) -> List[dict]:
        return [column.jsonify() for column in columns]

    def post(self: 'ColumnController', column_id: int) -> Response:
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

    # TODO: create put method

    def validate_body(self: 'ColumnController', body: dict) -> Tuple[str, str]:
        project_id, raw_columns = body.get('project_id'), body.get('raw_columns')

        if not project_id or not raw_columns:
            raise ValueError('Missing required fields in body. Required fields: project_id, raw_columns.')

        return project_id, raw_columns
