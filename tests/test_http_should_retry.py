import requests
from collections.abc import Callable

import ai_intelligence_platform.ingestion.http as http
from ai_intelligence_platform.ingestion.http import get_source_response

class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "name": "test",
            "website": "https://example.com",
            "founded_year": 2021,
        }


connection_error = requests.exceptions.ConnectionError()

responses = iter([connection_error, FakeResponse()])

def fake_get(*args, **kwargs):
    response = next(responses)

    if isinstance(response,Exception):
        raise response

    return response

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
RUNTIME_ERROR = "Request failed"

URL = "https://example.com"
params={"name": "test"}

def always_retry(error):
    return True

def test_get_source_response_retries_then_succeeds(monkeypatch):
    monkeypatch.setattr(
        http.requests,
        "get",
        fake_get,
    )

    response = get_source_response(URL, params, MAX_RETRIES, RETRY_DELAY_SECONDS, always_retry, RUNTIME_ERROR)

    assert response["name"] == "test"