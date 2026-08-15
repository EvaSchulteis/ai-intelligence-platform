import pytest
import requests
from collections.abc import Callable

import ai_intelligence_platform.ingestion.http as http
from ai_intelligence_platform.ingestion.http import get_source_response


connection_error = requests.exceptions.ConnectionError()

responses = iter([connection_error])

def fake_get(*args, **kwargs):
    response = next(responses)

    if isinstance(response,Exception):
        raise response

    return response

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

URL = "https://example.com"
params={"name": "test"}

def never_retry(error):
    return False

def test_get_source_response_raise_error(monkeypatch):
    monkeypatch.setattr(
        http.requests,
        "get",
        fake_get,
    )


    with pytest.raises(requests.exceptions.ConnectionError):
        get_source_response(
            URL,
            params,
            MAX_RETRIES,
            RETRY_DELAY_SECONDS,
            never_retry
        )