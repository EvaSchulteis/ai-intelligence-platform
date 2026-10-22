from dataclasses import dataclass

@dataclass
class GitHubCollectionFailure:
    repository_id: str
    repository_name: str
    error_message: str