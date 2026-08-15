from ai_intelligence_platform.domain import Company
from ai_intelligence_platform.domain import CompanySourceError
from ai_intelligence_platform.domain import CompanyNotFoundError

def fetch_company(company_name:str, sources: list) -> Company:

    for source in sources:

        try:
            company = source(company_name)
            return company

        except CompanySourceError as error:
            continue

    raise CompanyNotFoundError("All company sources failed")