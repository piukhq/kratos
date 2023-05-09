from settings import settings
from tempfile import NamedTemporaryFile
from azure.core.exceptions import ServiceRequestError, ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from requests.adapters import HTTPAdapter


def _write_tmp_files(key: str, cert: str):
    paths = []
    for data in (key, cert):
        file = NamedTemporaryFile(delete=False)
        paths.append(file.name)
        file.write(data.encode())
        file.close()
    return tuple(paths)

def connect_to_vault() -> SecretClient:
    if settings.keyvault_url is None:
        raise Exception("Vault Error: settings.KEY_VAULT not set")

    try: 
        return SecretClient(vault_url=settings.keyvault_url, credential=DefaultAzureCredential())
    except ResourceNotFoundError:
        return SecretClient(vault_url=settings.arch_keyvault_url, credential=DefaultAzureCredential())
         
