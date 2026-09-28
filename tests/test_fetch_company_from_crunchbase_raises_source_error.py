import pytest
import requests

import ai_intelligence_platform.ingestion.crunchbase as crunchbase
from ai_intelligence_platform.domain import CompanySourceError

def fake_response(*args, **kwargs):
    raise requests.exceptions.ConnectionError

def test_get_source_response_success(monkeypatch):
    monkeypatch.setattr(
        crunchbase,
        "get_source_response",
        fake_response,
    )

    with pytest.raises(CompanySourceError) as error:
            crunchbase.fetch_company_from_crunchbase("Anthropic")

    assert isinstance(
         error.value.__cause__,
         requests.exceptions.ConnectionError,
    )

