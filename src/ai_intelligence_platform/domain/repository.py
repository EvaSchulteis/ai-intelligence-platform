from dataclasses import dataclass

@dataclass
class Repository:
    repository_id: str
    github_organization_id: str
    name: str