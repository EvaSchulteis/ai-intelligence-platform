from ai_intelligence_platform.domain import GitHubOrganization

def test_github_organization():
    github_org = GitHubOrganization(
        github_organization_id="3222",
        login="apple",
        name="Apple"
    )

    assert isinstance(github_org, GitHubOrganization)
    assert github_org.github_organization_id == "3222"
    assert github_org.login == "apple"
    assert github_org.name == "Apple"
    