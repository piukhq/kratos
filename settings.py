from pydantic import BaseSettings


class Settings(BaseSettings):
    keyvault_url: str
    auth_token: str = "25556b98-9488-4c53-b0c6-682ae562321e"
    amex_auth_token: str = "5ca1870e-69a9-41b8-bbee-d7ee7d14f502"
    amex_hostname: str = "https://api.americanexpress.com"

settings = Settings()
