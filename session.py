import json
import pytest
from requests import Session
from pydantic import ValidationError


class HTTPSession(Session):
    @classmethod
    def send_request(cls, request_type, endpoint, model, **params):
        response = request_type(endpoint, **params)
        response_text = json.loads(response.text)
        cls.validate_response(response_text, model)
        return response.status_code, response_text

    @classmethod
    def validate_response(cls, response_text, model):
        try:
            return model(**response_text)
        except ValidationError as e:
            pytest.fail(f"Validation failed: {e}")


class RequestTypes(object):
    GET = HTTPSession().get


class Endpoints(object):
    BASE_URL = 'https://cat-fact.herokuapp.com'
    FACTS = BASE_URL + '/facts'


class StatusCodes(object):
    HTTP_OK = 200
