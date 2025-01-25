from session import Endpoints, RequestTypes, StatusCodes
from tests.tests_random_facts.random_facts_models import RandomFactsModel

ENDPOINT = Endpoints.FACTS
PATH = f'{ENDPOINT}/random'

class TestRandomFacts:
    def test_api_status_code(self, http_object):
        status_code, _ = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        assert status_code == StatusCodes.HTTP_OK
