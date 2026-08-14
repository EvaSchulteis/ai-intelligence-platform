import requests
import time

from ai_intelligence_platform.domain import Company
from ai_intelligence_platform.ingestion.http import get_source_response

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
RUNTIME_ERROR = "Could not retrieve company data from Crunchbase"

URL = "https://this-domain-should-not-exist-123456789.com"


def fetch_company_from_crunchbase(company_name: str) -> Company:
    params={"name": company_name}

    crunchbase_response = get_source_response(URL, params, MAX_RETRIES, RETRY_DELAY_SECONDS, should_retry, RUNTIME_ERROR)
    return Company(
        name=crunchbase_response["name"],
    )

def should_retry(error):
    if isinstance(error, requests.exceptions.ConnectionError):
        return True

    if isinstance(error, requests.exceptions.HTTPError):
        if error.response is None:
            return False

        if 500 <= error.response.status_code < 600:
            return True

    return False
