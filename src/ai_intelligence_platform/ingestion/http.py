import requests
import time
from collections.abc import Callable

def get_source_response(url: str, params: dict, max_retries: int, retry_delay_seconds: int, should_retry: Callable, runtime_error: str) -> dict:

    last_error = None

    for attempt in range(max_retries):

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as error:
            last_error = error

            if should_retry(error):
                print(f"Attempt {attempt + 1} failed")
                time.sleep(retry_delay_seconds)
                print("Retrying...")
            else:
                raise error

    raise RuntimeError(
        runtime_error
    ) from last_error