from dataclasses import dataclass
from datetime import datetime


@dataclass
class RepositoryLanguageObservation:
    repository_id: str
    language: str
    bytes: int
    observed_at: datetime
    loaded_at: datetime


