from dataclasses import dataclass

from ai_intelligence_platform.domain.repository_language_observation import RepositoryLanguageObservation
from ai_intelligence_platform.domain.github_collection_failure import GitHubCollectionFailure

@dataclass
class GitHubCollectionResult:
    observations: list[RepositoryLanguageObservation]
    failures: list[GitHubCollectionFailure]

    @property
    def observation_count(self) -> int:
        return len(self.observations)
    
    @property
    def failure_count(self) -> int:
        return len(self.failures)
    
    