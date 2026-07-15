from ai_intelligence_platform.domain import Company

MOCK_COMPANIES = {
    "Anthropic": {
        "name": "Anthropic",
        "website": "https://anthropic.com",
        "founded_year": 2021,
    },
}

def fetch_company_from_crunchbase(company_name: str) -> Company:
    crunchbase_response = MOCK_COMPANIES[company_name]
    return Company(
        name=crunchbase_response["name"]
    )