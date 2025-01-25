import pytest

from session import HTTPSession


@pytest.fixture(scope='session')
def http_object():
    return HTTPSession()
