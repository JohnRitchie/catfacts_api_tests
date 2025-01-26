import json
import allure
import pytest
from requests import Session, Response
from pydantic import ValidationError, BaseModel
from typing import Type, Tuple, Any, Dict


class HTTPSession:
    def __init__(self):
        self.session = Session()

    @allure.step("Sending {method} request to {url}")
    def send_request(
        self, method: str, url: str, model: Type[BaseModel], **kwargs: Any
    ) -> tuple[int, BaseModel]:
        """
        Sends an HTTP request and validates the response.

        :param method: HTTP method (GET, POST, etc.)
        :param url: Endpoint URL
        :param model: Pydantic model to validate response
        :param kwargs: Additional parameters (headers, params, data, etc.)
        :return: Tuple of (status_code, validated response data)
        """
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            self.log_request_response(response, kwargs)
            response_data = self.parse_response(response)
            validated_data = self.validate_response(response_data, model)
            return response.status_code, validated_data
        except ValidationError as e:
            pytest.fail(f"Response validation failed: {e}")
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON response from {url}: {response.text}")
        except Exception as e:
            pytest.fail(f"Request failed: {e}")

    @staticmethod
    @allure.step("Parsing response")
    def parse_response(response: Response) -> Dict[str, Any]:
        """
        Parses JSON response safely.

        :param response: Response object
        :return: Parsed JSON data as dictionary
        """
        return response.json()

    @staticmethod
    @allure.step("Validating response with Pydantic model")
    def validate_response(response_data: Dict[str, Any], model: Type[BaseModel]) -> BaseModel:
        """
        Validates response against a Pydantic model.

        :param response_data: JSON data from response
        :param model: Pydantic model
        :return: Validated data
        """
        return model(**response_data)

    @staticmethod
    @allure.step("Logging request and response")
    def log_request_response(response: Response, request_kwargs: Dict[str, Any]):
        """
        Logs request and response details to Allure.
        :param response: Response object
        :param request_kwargs: Additional request parameters
        """
        allure.attach(
            json.dumps(request_kwargs, indent=2),
            name="Request Parameters",
            attachment_type=allure.attachment_type.JSON,
        )

        allure.attach(
            json.dumps(dict(response.request.headers), indent=2),
            name="Request Headers",
            attachment_type=allure.attachment_type.JSON,
        )

        allure.attach(
            json.dumps(response.json(), indent=2),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        allure.attach(
            f"Status Code: {response.status_code}",
            name="Response Status Code",
            attachment_type=allure.attachment_type.TEXT,
        )


class RequestTypes:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class Endpoints:
    BASE_URL = "https://cat-fact.herokuapp.com"
    FACTS = f"{BASE_URL}/facts"


class StatusCodes:
    HTTP_OK = 200
    HTTP_NOT_FOUND = 404
