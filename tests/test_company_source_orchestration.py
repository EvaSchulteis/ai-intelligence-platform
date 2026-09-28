from ai_intelligence_platform.ingestion.company_source import fetch_company
from ai_intelligence_platform.domain import Company


def fake_crunchbase(company_name):
    return Company(name="Anthropic")

def fake_clearbit(company_name):
    raise AssertionError("Clearbit should not have been called")

company_name = 'Anthropic'
sources = [fake_crunchbase, fake_clearbit]

def test_fetch_company_uses_first_successful_source():
    company = fetch_company(
        company_name,
        sources,
    )

    assert company.name == "Anthropic"