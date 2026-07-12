from ai_intelligence_platform.domain import Company

def fetch_company_from_crunchbase(company_name: str) -> Company:
    return Company(name=company_name)