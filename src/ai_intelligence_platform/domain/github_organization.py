from dataclasses import dataclass

@dataclass
class GitHubOrganization:
    github_organization_id: str
    login: str
    name: str
