import ai_intelligence_platform.ingestion.github as github

from ai_intelligence_platform.domain import Repository
from ai_intelligence_platform.domain import GitHubOrganization


def fake_response(url, params, *args):
    page = params["page"]

    if page == 1:
        return [{
            "id": 3222,
            "name": "media",
        }]
    elif page == 2:
        return [{
            "id": 15930,
            "name": "hubahuba",
        }]
    return []

fake_organization = GitHubOrganization(
    github_organization_id="9919",
    login="github",
    name="GitHub",
)

def test_fetch_repositories_from_github_returns_repositories(monkeypatch):

    monkeypatch.setattr(
        github,
        "get_source_response",
        fake_response,
    )
    monkeypatch.setattr(
        github,
        "PER_PAGE",
        1,
    )

    repositories = github.fetch_repositories(fake_organization)

    assert isinstance(repositories, list)
    assert all(isinstance(repository, Repository) for repository in repositories)
    assert len(repositories) == 2
    assert repositories[0].repository_id == "3222"
    assert repositories[0].github_organization_id == "9919"
    assert repositories[0].name == "media"
    assert repositories[1].repository_id == "15930"
    assert repositories[1].github_organization_id == "9919"
    assert repositories[1].name == "hubahuba"
    
