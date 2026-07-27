import requests

from ai_intelligence_platform.ingestion.crunchbase import should_retry

def test_connection_error_should_retry():
    connection_error = requests.exceptions.ConnectionError()

    assert should_retry(connection_error) is True

def test_connection_error_should_not_retry():
    http_error = requests.exceptions.HTTPError()

    assert should_retry(http_error) is False