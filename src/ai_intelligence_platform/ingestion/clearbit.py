import requests
import time

from ai_intelligence_platform.domain import Company

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

URL = "https://fake-clearbit-domain-123456789.com"

def fetch_company_from_clearbit(company_name: str) -> Company:
    clearbit_response = get_clearbit_response(company_name)
    return Company(
        name=clearbit_response["name"],
    )

def get_clearbit_response(company_name: str) -> dict:
    url = URL
    last_error = None

    for attempt in range(MAX_RETRIES):

        try:
            response = requests.get(url, params={"name": company_name})
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
        "Could not retrieve company data from Clearbit"
    ) from last_error

def should_retry(error):
    if isinstance(error, requests.exceptions.ConnectionError):
        return True

    if isinstance(error, requests.exceptions.HTTPError):
        if error.response is None:
            return False

        if 500 <= error.response.status_code < 600:
            return True

    return False