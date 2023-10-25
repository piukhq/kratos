from azure.core.exceptions import ServiceRequestError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests
from urllib.parse import urlencode, urljoin
from settings import settings

import json

credential = DefaultAzureCredential()
kv_client = SecretClient(vault_url=settings.keyvault_url, credential=credential)
base_url=settings.stonegate_atreemo_url;
stonegate_auth = {
    "username": json.loads(kv_client.get_secret("stonegate-compound-key-join").value)["username"],
    "password": json.loads(kv_client.get_secret("stonegate-compound-key-join").value)["password"],
}

class StonegateFindByEmail:

    def call_auth_endpoint(self):
        url = urljoin(base_url, "token")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "password",
            "username": stonegate_auth["username"],
            "password": stonegate_auth["password"],
        }
        payload = urlencode(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)

    def on_get(self, req, resp):
        bearer_token = f'Bearer ' + self.call_auth_endpoint()["access_token"]
        url = "https://rihanna.atreemo.uk/api/Customer/FindCustomerDetails"
        email = self.get_email_from_query_params(req)

        payload = json.dumps({
        "SearchFilters": {
            "Email": email
        },
        "ResponseFilters": {
            "LoyaltyDetails": True,
            "StaffInfo": True,
            "SupInfo": True
        },
        "BrandID": "Bink"
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    def get_email_from_query_params(self, req):
        for key, value in req.params.items():
            if key == "email":
                return value