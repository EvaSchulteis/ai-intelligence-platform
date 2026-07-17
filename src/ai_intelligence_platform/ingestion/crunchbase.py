import json

from ai_intelligence_platform.domain import Company

MOCK_CRUNCHBASE_RESPONSES = {
    "Anthropic": """
    {
        "name": "Anthropic",
        "website": "https://anthropic.com",
        "founded_year": 2021
    }
    """,
}

def fetch_company_from_crunchbase(company_name: str) -> Company:
    crunchbase_response = get_crunchbase_response(company_name)
    return Company(
        name=crunchbase_response["name"],
    )

def get_crunchbase_response(company_name: str) -> dict:
    crunchbase_response_text = MOCK_CRUNCHBASE_RESPONSES[company_name]
    crunchbase_response = json.loads(crunchbase_response_text)
    return crunchbase_response