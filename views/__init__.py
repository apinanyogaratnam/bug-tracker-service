from flask import Flask
from flask_restful import Api

from controllers.Root import Root


def create_app():
    app = Flask(__name__)
    api = Api(app)

    VERSION = 'api/v1'

    api.add_resource(Root, '/', f'/{VERSION}/')

    return app
