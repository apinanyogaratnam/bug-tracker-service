from flask import Flask
from flask_restful import Api

from controllers.utility import BaseAPI
from controllers.root import Root
from controllers.user_controller import UsersController


def create_app():
    app = Flask(__name__)
    api = Api(app)

    VERSION = 'api/v1'

    resource = {'base_api': BaseAPI}

    api.add_resource(Root, '/', f'/{VERSION}/')

    api.add_resource(UsersController, f'/{VERSION}/users/', resource_class_kwargs=resource)

    return app
