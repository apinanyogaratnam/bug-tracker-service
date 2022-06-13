from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from controllers.column_controller import ColumnController

from controllers.utility import BaseAPI
from controllers.Root import Root
from controllers.user_controller import UsersController
from controllers.project_controller import ProjectController


def create_app():
    app = Flask(__name__)
    api = Api(app)
    CORS(app)

    VERSION = 'api/v1'

    resource = {'base_api': BaseAPI()}

    api.add_resource(Root, '/', f'/{VERSION}/')

    # TODO: rename UsersController to UserController
    api.add_resource(
        UsersController,
        f'/{VERSION}/users', f'/{VERSION}/user/<string:email>', f'/{VERSION}/user',
        resource_class_kwargs=resource,
    )

    # TODO: change to projects/<int:project_id>
    api.add_resource(
        ProjectController,
        f'/{VERSION}/project/<int:project_id>',
        f'/{VERSION}/projects',
        f'/{VERSION}/project',
        resource_class_kwargs=resource,
    )

    api.add_resource(
        ColumnController,
        f'/{VERSION}/columns',
        f'/{VERSION}/column',
        f'/{VERSION}/column/<int:column_id>',
        resource_class_kwargs=resource,
    )

    # TODO: create endpoint for adding a new card to a column

    return app
