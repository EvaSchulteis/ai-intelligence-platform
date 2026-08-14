import requests
import time
from collections.abc import Callable

def get_source_response(URL: str, params: dict, MAX_RETRIES: int, RETRY_DELAY_SECONDS: int, should_retry: Callable, RUNTIME_ERROR: str) -> dict:

    last_error = None

    for attempt in range(MAX_RETRIES):

        try:
            response = requests.get(URL, params=params)
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
        RUNTIME_ERROR
    ) from last_error