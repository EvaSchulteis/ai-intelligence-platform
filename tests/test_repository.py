from ai_intelligence_platform.domain import Repository


def test_repository_language_observation():
    repositories = Repository(
        repository_id="1299",
        github_organization_id='3222',
        name="Apple",        
    )

    assert isinstance(repositories, Repository)
    assert repositories.repository_id == "1299"
    assert repositories.github_organization_id == "3222"
    assert repositories.name == "Apple"
    