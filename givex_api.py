from azure.core.exceptions import ServiceRequestError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json
from settings import settings 
import logging 
from utilities import connect_to_vault
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)


def load_credentials_from_vault():
    client = connect_to_vault()
    givex_username = client.get_secret("givex-username").value
    givex_password = client.get_secret("givex-password").value
    return givex_username, givex_password
