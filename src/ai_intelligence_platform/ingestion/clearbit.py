import requests
import time

from ai_intelligence_platform.domain import Company
from ai_intelligence_platform.ingestion.http import get_source_response

MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 10
RUNTIME_ERROR = "Could not retrieve company data from Clearbit"

URL = "https://fake_clearbit.com"


def fetch_company_from_clearbit(company_name: str) -> Company:
    params={"name": company_name}

    clearbit_response = get_source_response(URL, params, MAX_RETRIES, RETRY_DELAY_SECONDS, should_retry, RUNTIME_ERROR)
    return Company(
        name=clearbit_response["name"],
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