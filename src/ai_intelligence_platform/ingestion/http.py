import requests
import time

def get_source_response(company_name: str, URL: str, MAX_RETRIES: int, RETRY_DELAY_SECONDS: int, RUNTIME_ERROR: str) -> dict:

    url = URL
    last_error = None

    for attempt in range(MAX_RETRIES):

        try:
            response = requests.get(url, params={"name": company_name})
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            last_error = error

            if f"{company_name}_should_retry"(error):
                print(f"Attempt {attempt + 1} failed")
                time.sleep(RETRY_DELAY_SECONDS)
                print("Retrying...")
            else:
                raise error

    raise RuntimeError(
        RUNTIME_ERROR
    ) from last_error