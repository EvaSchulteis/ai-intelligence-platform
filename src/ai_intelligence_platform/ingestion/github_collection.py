from ai_intelligence_platform.domain import (
    RepositoryLanguageObservation,
    GitHubCollectionResult,
    GitHubCollectionFailure,
    GitHubRepositoryLanguageError,
)

from ai_intelligence_platform.ingestion.github import (
    fetch_github_organization,
    fetch_repositories,
    fetch_repository_language_observations,
)

def collect_github_data(login: str) -> GitHubCollectionResult:
    organization = fetch_github_organization(login)
    repositories = fetch_repositories(organization)
    

    observations: list[RepositoryLanguageObservation] = []
    failures: list[GitHubCollectionFailure] = []
    successful_repository_count: int = 0

    for repository in repositories:
        try:
            repo_observations = fetch_repository_language_observations(
                organization, repository
            )
            successful_repository_count += 1
            observations.extend(repo_observations)
        except GitHubRepositoryLanguageError as error:
            failures.append(
                GitHubCollectionFailure(
                    repository_id=repository.repository_id, 
                    repository_name=repository.name, 
                    error_message=str(error),
                )
            )

    return GitHubCollectionResult(
        observations=observations, 
        failures=failures,
        successful_repository_count=successful_repository_count
    )
