from collections.abc import Callable

import ai_intelligence_platform.ingestion.http as http
from ai_intelligence_platform.ingestion.http import get_source_response
from ai_intelligence_platform.ingestion.crunchbase import should_retry

class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "name": "Anthropic",
            "website": "https://anthropic.com",
            "founded_year": 2021,
        }

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
RUNTIME_ERROR = "Could not retrieve company data from Crunchbase"

URL = "https://this-domain-should-not-exist-123456789.com"
params={"name": "Anthropic"}

def fake_get(*args, **kwargs):
    return FakeResponse()

def test_get_source_response_success(monkeypatch):
    monkeypatch.setattr(
        http.requests,
        "get",
        fake_get,
    )

    response = get_source_response(URL, params, MAX_RETRIES, RETRY_DELAY_SECONDS, should_retry, RUNTIME_ERROR)

    assert response["name"] == "Anthropic"