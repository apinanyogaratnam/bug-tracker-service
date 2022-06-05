from flask import Flask
from flask_restful import Api

from controllers.utility import BaseAPI
from controllers.Root import Root
from controllers.user_controller import UsersController
from controllers.project_controller import ProjectController


def create_app():
    app = Flask(__name__)
    api = Api(app)

    VERSION = 'api/v1'

    resource = {'base_api': BaseAPI()}

    api.add_resource(Root, '/', f'/{VERSION}/')

    api.add_resource(
        UsersController,
        f'/{VERSION}/users', f'/{VERSION}/user/<string:email>', f'/{VERSION}/user',
        resource_class_kwargs=resource
    )

    api.add_resource(
        ProjectController,
        f'/{VERSION}/project/<int:project_id>',
        f'/{VERSION}/projects',
        resource_class_kwargs=resource
    )

    return app
