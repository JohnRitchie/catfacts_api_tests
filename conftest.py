import pytest

from session import HTTPSession


@pytest.fixture(scope='class')
def http_object():
    http_object = HTTPSession()
    return http_object
