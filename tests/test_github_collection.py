from datetime import datetime, timezone

import pytest

from ai_intelligence_platform.domain.errors import GitHubOrganizationError
import ai_intelligence_platform.ingestion.github_collection as collection

from ai_intelligence_platform.domain import (
    GitHubCollectionResult,
    GitHubOrganization,
    GitHubRepositoryError,
    GitHubRepositoryLanguageError,
    Repository,
    RepositoryLanguageObservation,
)

LOGIN = "github"
TZINFO = timezone.utc

def fake_fetch_organization(*args):
    return GitHubOrganization(
        github_organization_id="9919",
        login="github",
        name="GitHub",
    )


def fake_fetch_repositories(*args):
    return [
        Repository(
            repository_id="repo1",
            github_organization_id="9919",
            name="repo1",
        ),
        Repository(
            repository_id="repo2",
            github_organization_id="9919",
            name="repo2",
        ),
        Repository(
            repository_id="repo3",
            github_organization_id="9919",
            name="repo3",
        ),
    ]

def fake_fetch_languages(organization, repository):
    if repository.repository_id == "repo1":
        return [
            RepositoryLanguageObservation(
                repository_id="repo1",
                language="CoffeeScript",
                byte_count=1072779,
                observed_at=datetime(2026, 10, 15, 12, 0,0, tzinfo=TZINFO),
            ),
            RepositoryLanguageObservation(
                repository_id="repo1",
                language="JavaScript",
                byte_count=7030,
                observed_at=datetime(2026, 10, 15, 12, 0,0, tzinfo=TZINFO),
            ),
        ]
    elif repository.repository_id == "repo2":
        raise GitHubRepositoryLanguageError("Failed to fetch languages for repo2")
    elif repository.repository_id == "repo3":
        return [
            RepositoryLanguageObservation(
                repository_id="repo3",
                language="Python",
                byte_count=100000,
                observed_at=datetime(2026, 10, 15, 12, 0,0, tzinfo=TZINFO),
            )
        ]

def test_collection_continues_after_repository_language_failure(monkeypatch):
    monkeypatch.setattr(
        collection, "fetch_github_organization", fake_fetch_organization
    )

    monkeypatch.setattr(
        collection, "fetch_repositories", fake_fetch_repositories
    )

    monkeypatch.setattr(
        collection,
        "fetch_repository_language_observations", fake_fetch_languages
    )

    result = collection.collect_github_data("github")

    assert isinstance(result, GitHubCollectionResult)
    assert result.observation_count == 3
    assert result.failure_count == 1
    assert result.successful_repository_count == 2
    assert result.total_repositories_attempted == 3
    assert isinstance(result.failures[0], collection.GitHubCollectionFailure)
    assert result.failures[0].repository_id == "repo2"
    assert result.failures[0].error_message == "Failed to fetch languages for repo2"
    assert result.observations[0].repository_id == "repo1"
    assert result.observations[2].repository_id == "repo3"


def fake_fetch_repositories_success(*args):
    return [
        Repository(
            repository_id="repo1",
            github_organization_id="9919",
            name="repo1",
        ),
        Repository(
            repository_id="repo3",
            github_organization_id="9919",
            name="repo3",
        ),
    ]

def test_collection_all_success(monkeypatch):
    monkeypatch.setattr(
        collection, "fetch_github_organization", fake_fetch_organization
    )

    monkeypatch.setattr(
        collection, "fetch_repositories", fake_fetch_repositories_success
    )

    monkeypatch.setattr(
        collection,
        "fetch_repository_language_observations", fake_fetch_languages
    )

    result = collection.collect_github_data("github")

    assert isinstance(result, GitHubCollectionResult)
    assert result.observation_count == 3
    assert result.successful_repository_count == 2
    assert result.total_repositories_attempted == 2
    assert result.success_rate == 1.0
    assert result.observations[0].repository_id == "repo1"
    assert result.observations[2].repository_id == "repo3"
    assert result.failure_count == 0
    assert result.failures == []

def fake_fetch_languages_empty(organization, repository):
    if repository.repository_id == "repo1":
        return [
            RepositoryLanguageObservation(
                repository_id="repo1",
                language="CoffeeScript",
                byte_count=1072779,
                observed_at=datetime(2026, 10, 15, 12, 0,0, tzinfo=TZINFO),
            ),
            RepositoryLanguageObservation(
                repository_id="repo1",
                language="JavaScript",
                byte_count=7030,
                observed_at=datetime(2026, 10, 15, 12, 0,0, tzinfo=TZINFO),
            ),
        ]
    elif repository.repository_id == "repo2":
        return []
    elif repository.repository_id == "repo3":
        return [
            RepositoryLanguageObservation(
                repository_id="repo3",
                language="Python",
                byte_count=100000,
                observed_at=datetime(2026, 10, 15, 12, 0,0, tzinfo=TZINFO),
            )
        ]

def test_collection_empty_response(monkeypatch):
    monkeypatch.setattr(
        collection, "fetch_github_organization", fake_fetch_organization
    )

    monkeypatch.setattr(
        collection, "fetch_repositories", fake_fetch_repositories
    )

    monkeypatch.setattr(
        collection,
        "fetch_repository_language_observations", fake_fetch_languages_empty
    )

    result = collection.collect_github_data("github")

    assert isinstance(result, GitHubCollectionResult)
    assert result.observation_count == 3
    assert result.successful_repository_count == 3
    assert result.total_repositories_attempted == 3
    assert result.success_rate == 1.0
    assert result.observations[0].repository_id == "repo1"
    assert result.observations[2].repository_id == "repo3"
    assert result.failure_count == 0
    assert result.failures == []

def fake_fetch_languages_empty_responses(organization, repository):
    if repository.repository_id == "repo1":
        return []
    elif repository.repository_id == "repo2":
        return []
    elif repository.repository_id == "repo3":
        return []

def test_collection_all_repositories_return_empty_responses(monkeypatch):
    monkeypatch.setattr(
        collection, "fetch_github_organization", fake_fetch_organization
    )

    monkeypatch.setattr(
        collection, "fetch_repositories", fake_fetch_repositories
    )

    monkeypatch.setattr(
        collection,
        "fetch_repository_language_observations", fake_fetch_languages_empty_responses
    )

    result = collection.collect_github_data("github")

    assert isinstance(result, GitHubCollectionResult)
    assert result.observation_count == 0
    assert result.successful_repository_count == 3
    assert result.total_repositories_attempted == 3
    assert result.success_rate == 1.0
    assert result.failure_count == 0
    assert result.failures == []

def fake_fetch_no_repositories(*args):
    return []

def test_collection_no_repositories(monkeypatch):
    monkeypatch.setattr(
        collection, "fetch_github_organization", fake_fetch_organization
    )

    monkeypatch.setattr(
        collection, "fetch_repositories", fake_fetch_no_repositories
    )

    result = collection.collect_github_data("github")

    assert isinstance(result, GitHubCollectionResult)
    assert result.observation_count == 0
    assert result.successful_repository_count == 0
    assert result.total_repositories_attempted == 0
    assert result.success_rate is None
    assert result.failure_count == 0
    assert result.failures == []

def fake_fetch_organization_failure(*args):
    raise GitHubOrganizationError("Connection Error for organization github")

def test_github_organization_collection_failure(monkeypatch):
    monkeypatch.setattr(
        collection, "fetch_github_organization", fake_fetch_organization_failure
    )

    with pytest.raises(GitHubOrganizationError, match="Connection Error for organization github"):
        collection.collect_github_data(LOGIN)


def fake_fetch_repositories_failure(*args):
    raise GitHubRepositoryError("Connection Error about repositories for github on page 1")

def test_github_repositories_collection_failure(monkeypatch):
    monkeypatch.setattr(
        collection, "fetch_github_organization", fake_fetch_organization
    )

    monkeypatch.setattr(
        collection, "fetch_repositories", fake_fetch_repositories_failure
    )

    with pytest.raises(GitHubRepositoryError, match="Connection Error about repositories for github on page 1"):
        collection.collect_github_data(LOGIN)
