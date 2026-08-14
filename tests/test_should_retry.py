import requests

from ai_intelligence_platform.ingestion.crunchbase import should_retry

class FakeResponse: 
    def __init__(self, status_code): 
        self.status_code = status_code

def test_connection_error_should_retry():
    connection_error = requests.exceptions.ConnectionError()

    assert should_retry(connection_error) is True

def test_http_error_without_response_should_not_retry():
    http_error = requests.exceptions.HTTPError()

    assert should_retry(http_error) is False

def test_5xx_error_should_retry(): 
    fake_response = FakeResponse(503) 
    error = requests.exceptions.HTTPError() 
    error.response = fake_response 

    assert should_retry(error) is True

def test_4xx_error_should_not_retry():
    fake_response = FakeResponse(404)
    error = requests.exceptions.HTTPError()
    error.response = fake_response

    assert should_retry(error) is False

def test_unkown_error_should_not_retry():
    error = ValueError()

    assert should_retry(error) is False