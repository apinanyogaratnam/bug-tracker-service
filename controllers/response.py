import json

from flask import Response as FlaskResponse

FORMAT_TYPE: str = 'application/json'


class Response:
    """Response object wrapper of flask Response object"""
    def __new__(cls: 'Response', response_data: dict | list, status_code: int, message: str = None, error: str = None) -> FlaskResponse:
        """Constructor for Response class
        Args:
            response_data (object): response data
            status_code (int): status code
            message (str): message to be returned
            error (str): error to be returned
        Returns:
            Response: Flask Response object
        """
        if message is not None:
            response_data['message'] = message
        if error is not None:
            response_data['error'] = error

        response_data = json.dumps(response_data)
        return FlaskResponse(json.dumps(response_data), status=status_code, mimetype=FORMAT_TYPE)
