from flask_restful import Resource


class Root(Resource):
    def __init__(self) -> None:
        pass

    def get(self) -> dict:
        """Get the status of the API."""
        return {
            "status": "OK",
            "message": "Welcome to the API"
        }
