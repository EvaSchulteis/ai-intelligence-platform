import ai_intelligence_platform.ingestion.clearbit as clearbit

class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "name": "Anthropic",
            "website": "https://anthropic.com",
            "founded_year": 2021,
        }

def fake_get(url, params):
    return FakeResponse()

def test_get_clearbit_response_success(monkeypatch):
    monkeypatch.setattr(
        clearbit.requests,
        "get",
        fake_get,
    )

    response = clearbit.get_clearbit_response("Anthropic")

    assert response["name"] == "Anthropic"