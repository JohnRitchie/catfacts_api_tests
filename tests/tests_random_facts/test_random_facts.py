import allure
from concurrent.futures import ThreadPoolExecutor
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
        with allure.step("Send GET request"):
            status_code, _ = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate HTTP status code"):
            assert_that(status_code).is_equal_to(StatusCodes.HTTP_OK)

    @allure.title("Test API returns non-empty fact text")
    def test_non_empty_text(self, http_object):
        with allure.step("Send GET request"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate text of fact"):
            assert_that(data.text).is_not_empty()

    @allure.title("Test response body contains all expected fields")
    def test_response_contains_all_fields(self, http_object):
        with allure.step("Send GET request"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate response contains all expected fields"):
            required_fields = {
                field_name for field_name, field in RandomFactsModel.model_fields.items()
                if not field.is_required
            }
            actual_fields = set(data.model_dump().keys())
            missing_fields = required_fields - actual_fields
            assert_that(missing_fields).is_empty()

    @allure.title("Test API returns default type for request with default parameters")
    def test_default_parameters(self, http_object):
        with allure.step("Send GET request with default parameters"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate data type"):
            assert_that(data.type).is_equal_to('cat')

    @allure.title("Test API returns requested type for request with user parameters")
    def test_user_parameters(self, http_object):
        with allure.step("Send GET request with user parameters"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel, params={"animal_type": "horse"})
        with allure.step("Validate data type"):
            assert_that(data.type).is_equal_to('horse')

    @allure.title("Test API ignores unsupported parameters")
    def test_unsupported_parameters(self, http_object):
        with allure.step("Send GET request with unsupported parameters"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel,
                                               params={"unknown_param": "test"})
        with allure.step("Validate response ignores unsupported parameters"):
            assert_that(data.type).is_equal_to('cat')

    @allure.title("Test createdAt and updatedAt have correct format")
    def test_datetime_format(self, http_object):
        with allure.step("Send GET request"):
            _, data = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate datetime fields"):
            assert_that(data.createdAt).matches(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z")
            assert_that(data.updatedAt).matches(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z")

    @allure.title("Test response uses UTF-8 encoding")
    def test_response_encoding(self, http_object):
        with allure.step("Send GET request"):
            response = http_object.session.get(PATH)
        with allure.step("Validate response encoding"):
            assert_that(response.encoding).is_equal_to("utf-8")

    @allure.title("Test API does not cache responses")
    def test_no_caching(self, http_object):
        with allure.step("Send two GET requests"):
            _, data1 = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
            _, data2 = http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)
        with allure.step("Validate that responses are not cached"):
            assert_that(data1.text).is_not_equal_to(data2.text)

    @allure.title("Test multiple requests returns unique facts")
    def test_unique_facts(self, http_object):
        with allure.step("Send multiple GET requests"):
            facts = [http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel)[1].text for _ in range(10)]
        with allure.step("Validate that all facts are unique"):
            assert_that(facts).does_not_contain_duplicates()

    @allure.title("Test API handles high load of parallel requests")
    def test_high_load(self, http_object):
        # Warning! A load of 100 requests crashes the server, no more than 10 requests should be used for training
        with allure.step("Send multiple parallel GET requests"):
            with ThreadPoolExecutor(max_workers=10) as executor:
                responses = list(
                    executor.map(lambda _: http_object.send_request(RequestTypes.GET, PATH, RandomFactsModel),
                                 range(10)))
        with allure.step("Validate all responses are successful"):
            for status_code, _ in responses:
                assert_that(status_code).is_equal_to(StatusCodes.HTTP_OK)
