from datetime import datetime

from ai_intelligence_platform.domain import RepositoryLanguageObservation


def test_repository_language_observation():
    repolangobs = RepositoryLanguageObservation(
        repository_id="1299",
        language="Python",
        bytes=2021,
        observed_at=datetime(2026, 9, 24, 12, 31, 31),
        loaded_at=datetime(2026, 9, 25, 12, 31, 46),
    )

    assert isinstance(repolangobs, RepositoryLanguageObservation)
    assert repolangobs.repository_id == "1299"
    assert repolangobs.language == "Python"
    assert repolangobs.bytes == 2021
    assert repolangobs.observed_at == datetime(2026, 9, 24, 12, 31, 31)
    assert repolangobs.loaded_at == datetime(2026, 9, 25, 12, 31, 46)

