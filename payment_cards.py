import falcon
from settings import settings
import logging
from urllib.parse import urlencode, urljoin
from azure.core.exceptions import ServiceRequestError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests
from requests.auth import HTTPBasicAuth
import base64
logger = logging.getLogger(__name__)
import json

credential = DefaultAzureCredential()
kv_client = SecretClient(vault_url=settings.keyvault_url, credential=credential)


class PaymentCards:
    def call_auth_endpoint(self, client_id, username):

        b2c_auth = {
            "username": client_id,
            "password": json.loads(kv_client.get_secret("b2c-channel-keys").value)["data"][client_id],
         }

        url = urljoin(settings.v2_url, "token")
        headers = {
                "Content-Type": "application/json",
                 }
        payload = json.dumps({
           'grant_type': 'client_credentials',
            'username': username,
            'scope': [
                'user'
            ]
        })

        response = requests.request("POST", url, headers=headers, auth=HTTPBasicAuth(b2c_auth["username"], b2c_auth["password"]), data=payload)
        return json.loads(response.text)

    def on_delete(self, req, resp):
        auth_param = req.get_param('auth')

        if auth_param == settings.v2_auth_token:

            client_id = req.get_param('client_id')
            username = req.get_param('username')
            payment_card_id = req.get_param('payment_card_id')

            bearer_token = f'Bearer ' + self.call_auth_endpoint(client_id, username)["access_token"]
            url = urljoin(settings.v2_url, f"payment_accounts/{payment_card_id}")
            headers = {        
                'Content-Type': 'application/json',
                'Authorization': bearer_token
            }
            logger.error(f'URL -->> {url}')
            response = requests.request("DELETE", url, headers=headers)
            resp.status = response.status_code
            resp.content_type = falcon.MEDIA_JSON
            resp.media = json.loads(response.text)
        else:
            resp.status = falcon.HTTP_401
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "Access Denied"
