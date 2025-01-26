from assertpy import assert_that
from session import Endpoints, RequestTypes, StatusCodes
from tests.tests_random_facts.random_facts_models import RandomFactsModel

ENDPOINT = Endpoints.FACTS
PATH = f'{ENDPOINT}/random'

class TestRandomFacts:
    def test_status_code_ok(self, http_object):
        status_code, _ = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        assert_that(status_code).is_equal_to(StatusCodes.HTTP_OK)

    def test_random_fact_default_parameters(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        assert_that(data.type).is_equal_to('cat')

    def test_random_fact_user_parameters(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel, params={"animal_type": "horse"})
        assert_that(data.type).is_equal_to('horse')
