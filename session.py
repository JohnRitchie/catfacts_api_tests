import json
from requests import Session


class HTTPSession(Session):
    @staticmethod
    def send_request(request_type, endpoint, **params):
        response = request_type(endpoint, **params)
        return response.status_code, json.loads(response.text)


class RequestTypes(object):
    GET = HTTPSession().get


class Endpoints(object):
    BASE_URL = 'https://cat-fact.herokuapp.com'
    FACTS = BASE_URL + '/facts'


class StatusCodes(object):
    HTTP_OK = 200
