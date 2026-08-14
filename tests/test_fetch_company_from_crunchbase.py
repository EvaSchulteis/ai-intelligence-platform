import ai_intelligence_platform.ingestion.crunchbase as crunchbase

from ai_intelligence_platform.domain import Company


def fake_response(*args):
    return {
        "name": "Anthropic",
        "website": "https://anthropic.com",
        "founded_year": 2021,
    }


def test_fetch_company_from_crunchbase_returns_company(monkeypatch):
    monkeypatch.setattr(
        crunchbase,
        "get_source_response",
        fake_response,
    )

    company = crunchbase.fetch_company_from_crunchbase("Anthropic")

    assert isinstance(company, Company)
    assert company.name == "Anthropic"