from dataclasses import dataclass

from ai_intelligence_platform.domain.repository_language_observation import RepositoryLanguageObservation
from ai_intelligence_platform.domain.github_collection_failure import GitHubCollectionFailure

@dataclass
class GitHubCollectionResult:
    observations: list[RepositoryLanguageObservation]
    failures: list[GitHubCollectionFailure]
    successful_repository_count: int
    
    @property
    def total_repositories_attempted(self) -> int:
        return len(self.failures) + self.successful_repository_count

    @property
    def success_rate(self) -> float | None:
        total_attempted = self.total_repositories_attempted
        if total_attempted == 0:
            return None
        return self.successful_repository_count / total_attempted

    @property
    def observation_count(self) -> int:
        return len(self.observations)
    
    @property
    def failure_count(self) -> int:
        return len(self.failures)
    
    