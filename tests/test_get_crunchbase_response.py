import ai_intelligence_platform.ingestion.crunchbase as crunchbase

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

def test_get_crunchbase_response_success(monkeypatch):
    monkeypatch.setattr(
        crunchbase.requests,
        "get",
        fake_get,
    )

    response = crunchbase.get_crunchbase_response("Anthropic")

    assert response["name"] == "Anthropic"