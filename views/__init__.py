from flask import Flask
from flask_restful import Api

from controllers.Root import Root


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Root, '/')

    return app
