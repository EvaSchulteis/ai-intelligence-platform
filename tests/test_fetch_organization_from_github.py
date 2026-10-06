import ai_intelligence_platform.ingestion.github as github

from ai_intelligence_platform.domain import GitHubOrganization


def fake_response(*args):
    return {
        "id": 9919,
        "login": "github",
        "name": "Github",
    }

def test_fetch_organization_from_github_returns_organization(monkeypatch):
    monkeypatch.setattr(
        github,
        "get_source_response",
        fake_response,
    )

    github_organization = github.fetch_github_organization("github")

    assert isinstance(github_organization, GitHubOrganization)
    assert github_organization.github_organization_id == "9919"
    assert github_organization.login == "github"
    assert github_organization.name == "Github"