import allure
from assertpy import assert_that
from session import Endpoints, RequestTypes, StatusCodes
from tests.tests_random_facts.random_facts_models import RandomFactsModel

ENDPOINT = Endpoints.FACTS
PATH = f'{ENDPOINT}/random'

@allure.feature("Cat facts API")
@allure.suite("Random Facts API")
class TestRandomFacts:
    @allure.title("Test returns status 200")
    def test_status_code_ok(self, http_object):
        with allure.step("Send GET request"):
            status_code, _ = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate HTTP status code"):
            assert_that(status_code).is_equal_to(StatusCodes.HTTP_OK)

    @allure.title("Test returns default type for request with default parameters")
    def test_default_parameters(self, http_object):
        with allure.step("Send GET request with default parameters"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate data type"):
            assert_that(data.type).is_equal_to('cat')

    @allure.title("Test returns requested type for request with user parameters")
    def test_user_parameters(self, http_object):
        with allure.step("Send GET request with user parameters"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel, params={"animal_type": "horse"})
        with allure.step("Validate data type"):
            assert_that(data.type).is_equal_to('horse')

    @allure.title("Test returns non-empty fact text")
    def test_non_empty_text(self, http_object):
        with allure.step("Send GET request"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate text of fact"):
            assert_that(data.text).is_not_empty()

    @allure.title("Test createdAt and updatedAt have correct format")
    def test_datetime_format(self, http_object):
        with allure.step("Send GET request"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate datetime fields"):
            assert_that(data.createdAt).matches(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z")
            assert_that(data.updatedAt).matches(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z")

