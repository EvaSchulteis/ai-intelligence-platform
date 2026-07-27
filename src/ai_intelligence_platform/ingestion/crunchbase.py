import requests
import time

from ai_intelligence_platform.domain import Company

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

MOCK_CRUNCHBASE_RESPONSES = {
    "Anthropic": """
    {
        "name": "Anthropic",
        "website": "https://anthropic.com",
        "founded_year": 2021
    }
    """,
}

def fetch_company_from_crunchbase(company_name: str) -> Company:
    crunchbase_response = get_crunchbase_response(company_name)
    return Company(
        name=crunchbase_response["name"],
    )

def get_crunchbase_response(company_name: str) -> dict:
    url = "https://this-domain-should-not-exist-123456789.com"
    last_error = None

    for attempt in range(MAX_RETRIES):

        try:
            response = requests.get(url, params={"name":company_name})
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            last_error = error

            if should_retry(error):
                print(f"Attempt {attempt + 1} failed")
                time.sleep(RETRY_DELAY_SECONDS)
                print("Retrying...")
            else:
                raise error

    raise RuntimeError(
        "Could not retrieve company data from Crunchbase"
    ) from last_error

def should_retry(error):
    return isinstance(error, requests.exceptions.ConnectionError)