import allure
from assertpy import assert_that
from session import Endpoints, RequestTypes, StatusCodes
from tests.tests_random_facts.random_facts_models import RandomFactsModel

ENDPOINT = Endpoints.FACTS
PATH = f'{ENDPOINT}/random'

@allure.feature("Cat facts API")
@allure.suite("Random Facts API")
class TestRandomFacts:
    @allure.title("Test API returns status 200")
    def test_status_code_ok(self, http_object):
        with allure.step("Send GET request to /random endpoint"):
            status_code, _ = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate HTTP status code"):
            assert_that(status_code).is_equal_to(StatusCodes.HTTP_OK)

    @allure.title("Test API returns default type for request with default parameters")
    def test_random_fact_default_parameters(self, http_object):
        with allure.step("Send GET request to /random endpoint with default parameters"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate data type"):
            assert_that(data.type).is_equal_to('cat')

    @allure.title("Test API returns requested type for request with user parameters")
    def test_random_fact_user_parameters(self, http_object):
        with allure.step("Send GET request to /random endpoint with user parameters"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel, params={"animal_type": "horse"})
        with allure.step("Validate data type"):
            assert_that(data.type).is_equal_to('horse')
