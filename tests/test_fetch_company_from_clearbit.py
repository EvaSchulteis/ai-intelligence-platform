import ai_intelligence_platform.ingestion.clearbit as clearbit

from ai_intelligence_platform.domain import Company

def fake_response(*args):
    return {
        "name": "Anthropic",
        "website": "https://anthropic.com",
        "founded_year": 2021,
    }


def test_fetch_company_from_clearbit_returns_company(monkeypatch):
    monkeypatch.setattr(
        clearbit,
        "get_source_response",
        fake_response,
    )

    company = clearbit.fetch_company_from_clearbit("Anthropic")

    assert isinstance(company, Company)
    assert company.name == "Anthropic"