from pydantic import BaseSettings


class Settings(BaseSettings):
    keyvault_url: str
    auth_token: str = "25556b98-9488-4c53-b0c6-682ae562321e"


settings = Settings()
