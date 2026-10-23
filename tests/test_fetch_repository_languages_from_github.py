from datetime import timezone

import ai_intelligence_platform.ingestion.github as github
from ai_intelligence_platform.domain import RepositoryLanguageObservation
from ai_intelligence_platform.domain import Repository
from ai_intelligence_platform.domain import GitHubOrganization


def fake_response(*args):
    return {
    "CoffeeScript": 1072779,
    "JavaScript": 7030
    }

fake_organization = GitHubOrganization(
    github_organization_id="9919",
    login="github",
    name="GitHub",
)

fake_repository = Repository(
    repository_id="3222",
    github_organization_id="9919",
    name="media",
)

def test_fetch_repository_languages_from_github(monkeypatch):

    monkeypatch.setattr(
        github,
        "get_source_response",
        fake_response,
    )

    observations = github.fetch_repository_language_observations(fake_organization, fake_repository)

    assert isinstance(observations, list)
    assert len(observations) == 2
    assert observations[0].observed_at.tzinfo == timezone.utc
    assert observations[0].observed_at == observations[1].observed_at
    assert all(
        isinstance(observation, RepositoryLanguageObservation) 
        for observation in observations
    )
    assert observations[0].repository_id == "3222"
    assert observations[0].language == "CoffeeScript"
    assert observations[0].byte_count == 1072779
    assert observations[1].repository_id == "3222"
    assert observations[1].language == "JavaScript"
    assert observations[1].byte_count == 7030
    


def fake_empty_response(*args):
    return {}

def test_fetch_repository_languages_from_github_empty(monkeypatch):

    monkeypatch.setattr(
        github,
        "get_source_response",
        fake_empty_response,
    )

    observations = github.fetch_repository_language_observations(fake_organization, fake_repository)

    assert isinstance(observations, list)
    assert len(observations) == 0