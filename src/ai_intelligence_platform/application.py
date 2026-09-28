from ai_intelligence_platform.ingestion.company_source import fetch_company
from ai_intelligence_platform.ingestion.crunchbase import fetch_company_from_crunchbase
from ai_intelligence_platform.ingestion.clearbit import fetch_company_from_clearbit

def main():
    sources = [
        fetch_company_from_crunchbase,
        fetch_company_from_clearbit,
    ]

    company = fetch_company("Anthropic", sources)
    print(company)