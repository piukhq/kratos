from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    keyvault_url: str
    arch_keyvault_url: str = "https://functionkeyvvault.vault.azure.net/"
    visa_auth_token: str = "25556b98-9488-4c53-b0c6-682ae562321e"
    v2_auth_token: str = "5581aec3-fd25-4bc1-bf12-a174d6df0a69"
    v2_url: str = "https://api.staging.gb.bink.com/v2/"
    givex_auth_token: str = "d4a0b0b8-dc27-4ba0-8be0-5fb98ab34f11"
    sgg_auth_token: str = "30b03847-9422-4c87-9477-e765bad7cc84"
    visa_community_code: str = "BINK"
    amex_auth_token: str = "5ca1870e-69a9-41b8-bbee-d7ee7d14f502"
    amex_hostname: str = "https://apigateway2s.americanexpress.com"
    stonegate_atreemo_url = "https://rihanna.atreemo.uk"

    # Punchh (TGIF) API 
    punchh_api_url: str = "https://dashboard.punchh.com"

settings = Settings()
