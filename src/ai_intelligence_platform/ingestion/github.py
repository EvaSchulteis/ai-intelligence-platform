import requests

from ai_intelligence_platform.domain import GitHubOrganization
from ai_intelligence_platform.domain import GitHubOrganizationError
from ai_intelligence_platform.domain import Repository
from ai_intelligence_platform.domain import GitHubRepositoryError
from ai_intelligence_platform.ingestion.http import get_source_response


MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
BASE_URL = "https://api.github.com/orgs/"



def fetch_github_organization(login: str) -> GitHubOrganization:
    params={}
    URL = f"{BASE_URL}{login}"
    RUNTIME_ERROR = "Could not retrieve organization data from GitHub"

    try:
        github_response = get_source_response(
            URL, 
            params,
            MAX_RETRIES,
            RETRY_DELAY_SECONDS,
            should_retry,
        )
    except requests.exceptions.RequestException as error:
        raise GitHubOrganizationError(
            RUNTIME_ERROR
        ) from error

    return GitHubOrganization(
        github_organization_id=str(github_response["id"]),
        login=github_response["login"],
        name=github_response["name"],
    )

def fetch_repositories(organization: GitHubOrganization) -> list[Repository]:
    params = {}
    URL = f"{BASE_URL}{organization.login}/repos"
    RUNTIME_ERROR = "Could not retrieve repository data from GitHub"
    repositories = []

    try:
        github_response = get_source_response(
            URL, 
            params,
            MAX_RETRIES,
            RETRY_DELAY_SECONDS,
            should_retry,
        )
    except requests.exceptions.RequestException as error:
        raise GitHubRepositoryError(
            RUNTIME_ERROR
        ) from error

    for response in github_response:
        # pull out the required information from the response
        repository = Repository(
            repository_id=str(response["id"]),
            github_organization_id=str(organization.github_organization_id),
            name=response["name"],
        )

        repositories.append(repository)

    return repositories


def should_retry(error):
    if isinstance(error, requests.exceptions.ConnectionError):
        return True

    if isinstance(error, requests.exceptions.HTTPError):
        if error.response is None:
            return False

        if 500 <= error.response.status_code < 600:
            return True

    return False
