from multiprocessing import context
import logging 
import hmac
import base64
import hashlib
import logging
from datetime import datetime
import json
import requests
from urllib.parse import urlsplit
from settings import settings
import uuid
import time
import typing as t
from urllib3.util.retry import Retry
from tempfile import NamedTemporaryFile

from azure.core.exceptions import ServiceRequestError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from requests.adapters import HTTPAdapter


import json

logger = logging.getLogger(__name__)

class RetryAdapter(HTTPAdapter):
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        retries: int = 3
        status_forcelist: t.Tuple = (500, 503, 504)
        retry = Retry(
            total=3,
            read=3,
            connect=retries,
            backoff_factor=0.3,
            status_forcelist=status_forcelist,
            raise_on_status=False,
        )
        kwargs["max_retries"] = retry
        super().__init__(*args, **kwargs)

def search_amex_merchants(request_body):
    session = requests.Session()
    session.mount(settings.amex_hostname, RetryAdapter())
    return _call_api("POST", "/marketing/v4/smartoffers/merchant/inquiry_results", session, request_body)


def _call_api(method: str, resource_uri: str, session, data: dict = None):
    
    client_priv_path, client_cert_path = load_cert_from_vault()

    payload = json.dumps(data)
    headers = _make_headers(method, resource_uri, payload)
    now = datetime.now()
    timestamp = datetime.timestamp(now)

    response = getattr(session, method.lower())(
        settings.amex_hostname + resource_uri,
        cert=(client_cert_path, client_priv_path),
        headers=headers,
        data=payload,
        timeout=(3.05, 10),
    )
    return response


def _make_headers(httpmethod: str, resource_uri: str, payload: str) -> dict:
    current_time_ms = str(round(time.time() * 1000))
    nonce = str(uuid.uuid4())
    client_id, client_secret = client_id_and_secret()

    bodyhash = base64.b64encode(
        hmac.new(client_secret.encode(), payload.encode(), digestmod=hashlib.sha256).digest()
    ).decode()

    hash_key_secret = (
        f"{current_time_ms}\n{nonce}\n{httpmethod.upper()}\n"
        f"{resource_uri}\n{urlsplit(settings.amex_hostname).netloc}\n443\n{bodyhash}\n"
    )
    mac = base64.b64encode(
        hmac.new(client_secret.encode(), hash_key_secret.encode(), digestmod=hashlib.sha256).digest()
    ).decode()

    return {
        "Content-Type": "application/json",
        "X-AMEX-API-KEY": client_id,
        "Authorization": f'MAC id="{client_id}",ts="{current_time_ms}"'
        f',nonce="{nonce}",bodyhash="{bodyhash}",mac="{mac}"',
    }

def client_id_and_secret():
    client = connect_to_vault()
    client_id = json.loads(client.get_secret("amex-clientId").value)["value"]
    client_secret = json.loads(client.get_secret("amex-clientSecret").value)["value"]
    return client_id, client_secret

def connect_to_vault() -> SecretClient:
    if settings.keyvault_url is None:
        raise Exception("Vault Error: settings.KEY_VAULT not set")

    return SecretClient(vault_url=settings.keyvault_url, credential=DefaultAzureCredential())

def load_cert_from_vault():
    client = connect_to_vault()
    client_cert_path = None
    client_priv_path = None

    try:
        client_priv_path, client_cert_path = _write_tmp_files(
            json.loads(client.get_secret("amex-cert").value)["key"],
            json.loads(client.get_secret("amex-cert").value)["cert"],
        )
    except ServiceRequestError:
        logger.error("Could not retrieve cert/key data from vault")

    return client_priv_path, client_cert_path


def _write_tmp_files(key: str, cert: str):
    paths = []
    for data in (key, cert):
        file = NamedTemporaryFile(delete=False)
        paths.append(file.name)
        file.write(data.encode())
        file.close()
    return tuple(paths)