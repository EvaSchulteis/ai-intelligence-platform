from ai_intelligence_platform.ingestion.crunchbase import (
    fetch_company_from_crunchbase,
)

def main():
    company = fetch_company_from_crunchbase("Anthropic")
    print(company)