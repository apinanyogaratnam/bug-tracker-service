from typing import Tuple

from flask import request
from flask_restful import Resource

from controllers.response import Response
from controllers.utility import BaseAPI
from models import Project


class ProjectController(Resource, Project):
    def __init__(self: 'ProjectController', base_api: BaseAPI) -> None:
        self.base_api = base_api

    def get(self: 'ProjectController', project_id: int = None) -> Response:
        if project_id is None:
            user_id: int = request.args.get('user_id', type=int, default=None)

            if user_id is None:
                return Response(
                    response_data={},
                    error='Missing required query parameter: user_id.',
                    message='Add a project id to the path or add a query parameter of user_id.',
                    status_code=400
                )

            projects: list = self.get_projects(user_id)
            return Response(response_data=projects, status_code=200)
        project = self.get_project(project_id)

        if project: return Response(response_data=project, status_code=200)

        return Response(response_data={}, error='Not Found', status_code=404)

    def get_project(self: 'ProjectController', project_id: int) -> dict:
        query_user: str = f'''
            SELECT
                project_id,
                user_id,
                administrator_id,
                co_administrator_ids,
                member_ids,
                name,
                description,
                EXTRACT(EPOCH FROM created_at) AS created_at
            FROM projects
            WHERE project_id = '{project_id}';
        '''

        project: list = self.base_api.create_pandas_table(query_user).to_dict(orient='records')

        return project[0] if project else None

    def get_projects(self: 'ProjectController', user_id: int) -> list:
        query_projects: str = f'''
            SELECT
                project_id,
                user_id,
                administrator_id,
                co_administrator_ids,
                member_ids,
                name,
                description,
                EXTRACT(EPOCH FROM created_at) AS created_at
            FROM projects
            WHERE user_id = '{user_id}'
            ORDER BY created_at DESC;
        '''

        projects: list = self.base_api.create_pandas_table(query_projects).to_dict(orient='records')

        return projects

    def post(self: 'ProjectController') -> Response:
        body: dict | list = request.get_json()

        try:
            user_id, name, description = self.validate_body(body)
        except ValueError as error:
            return Response(response_data={}, error=str(error), status_code=400)

        super().__init__(user_id, administrator_id=user_id, co_administrator_ids=[], member_ids=[], name=name, description=description)
        project: dict = self.create().jsonify()

        # TODO: Send email to user
        # TODO: update user's project_ids

        return Response(response_data=project, status_code=201)

    def validate_body(self: 'ProjectController', body: dict) -> Tuple[str, str, str]:
        user_id, name, description = body.get('user_id'), body.get('name'), body.get('description')

        if not user_id or not name or not description:
            raise ValueError('Missing required fields in body. Required fields: user_id, name, description')

        return user_id, name, description
