from dataclasses import dataclass
from datetime import datetime


@dataclass
class RepositoryLanguageObservation:
    repository_id: str
    language: str
    byte_count: int
    observed_at: datetime
