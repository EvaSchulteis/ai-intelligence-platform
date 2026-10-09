from datetime import datetime, timezone

import requests

from ai_intelligence_platform.domain import GitHubOrganization
from ai_intelligence_platform.domain import GitHubOrganizationError
from ai_intelligence_platform.domain import Repository
from ai_intelligence_platform.domain import GitHubRepositoryError
from ai_intelligence_platform.domain import RepositoryLanguageObservation
from ai_intelligence_platform.domain import GitHubRepositoryLanguageError
from ai_intelligence_platform.ingestion.http import get_source_response


MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2
BASE_URL = "https://api.github.com/orgs/"
PER_PAGE = 100
RUNTIME_ERROR = "Could not retrieve data from GitHub"


def fetch_github_organization(login: str) -> GitHubOrganization:
    params = {}
    url = f"{BASE_URL}{login}"

    try:
        github_response = get_source_response(
            url, 
            params,
            MAX_RETRIES,
            RETRY_DELAY_SECONDS,
            should_retry,
        )
    except requests.exceptions.RequestException as error:
        raise GitHubOrganizationError(
            f"{RUNTIME_ERROR} for organization {login}"
        ) from error

    return GitHubOrganization(
        github_organization_id=str(github_response["id"]),
        login=github_response["login"],
        name=github_response["name"],
    )

def fetch_repositories(organization: GitHubOrganization) -> list[Repository]:
    url = f"{BASE_URL}{organization.login}/repos"
    repositories = []
    page = 1

    while True:
        params = {"page": page, "per_page": PER_PAGE}
        try:
            github_response = get_source_response(
                url, 
                params,
                MAX_RETRIES,
                RETRY_DELAY_SECONDS,
                should_retry,
            )
        except requests.exceptions.RequestException as error:
            raise GitHubRepositoryError(
                f"{RUNTIME_ERROR} about repositories for {organization.login} on page {page}"
            ) from error

        for response in github_response:
            repository = Repository(
                repository_id=str(response["id"]),
                github_organization_id=str(organization.github_organization_id),
                name=response["name"],
            )

            repositories.append(repository)

        page += 1

        if len(github_response) < PER_PAGE:
            break

    return repositories

def fetch_repository_language_observations(
        organization: GitHubOrganization,
        repository: Repository,
) -> list[RepositoryLanguageObservation]:
    params = {}
    url = f"{BASE_URL}{organization.login}/{repository.name}/languages"

    try:
        github_response = get_source_response(
            url,
            params,
            MAX_RETRIES,
            RETRY_DELAY_SECONDS,
            should_retry,
        )
        retrieved_at = datetime.now(timezone.utc)

    except requests.exceptions.RequestException as error:
        raise GitHubRepositoryLanguageError(
            f"{RUNTIME_ERROR} for repository language observations from {repository.name}"
        ) from error

    return [
        RepositoryLanguageObservation(
            repository_id=repository.repository_id,
            language=language,
            byte_count=byte_count,
            observed_at=retrieved_at,
        )
        for language, byte_count in github_response.items()
    ]


def should_retry(error):
    if isinstance(error, requests.exceptions.ConnectionError):
        return True

    if isinstance(error, requests.exceptions.HTTPError):
        if error.response is None:
            return False

        if 500 <= error.response.status_code < 600:
            return True

    return False
