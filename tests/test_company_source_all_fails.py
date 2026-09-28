import pytest

from ai_intelligence_platform.ingestion.company_source import fetch_company
from ai_intelligence_platform.domain import CompanySourceError
from ai_intelligence_platform.domain import CompanyNotFoundError


def fake_crunchbase(company_name):
    raise CompanySourceError("Crunchbase failed")

def fake_clearbit(company_name):
    raise CompanySourceError("Clearbit failed")

company_name = 'Anthropic'
sources = [fake_crunchbase, fake_clearbit]

def test_fetch_company_raises_company_not_found_error_when_all_sources_fail():
    with pytest.raises(CompanyNotFoundError):
        fetch_company(company_name, sources)