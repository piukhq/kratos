from azure.core.exceptions import ServiceRequestError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests
from urllib.parse import urlencode, urljoin
from settings import settings
import falcon
import json
import logging
logger = logging.getLogger(__name__)



credential = DefaultAzureCredential()
kv_client = SecretClient(vault_url=settings.keyvault_url, credential=credential)
base_url=settings.stonegate_atreemo_url;
stonegate_auth = {
    "username": json.loads(kv_client.get_secret("stonegate-outbound-compound-key-join").value)["data"]["username"],
    "password": json.loads(kv_client.get_secret("stonegate-outbound-compound-key-join").value)["data"]["password"],
}


class Stonegate:

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

class StonegateFindByEmail(Stonegate):

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

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.media = json.loads(response.text)

    def get_email_from_query_params(self, req):
        for key, value in req.params.items():
            if key == "email":
                return value
            
class StonegateFindByMemberNumber(Stonegate):

    def on_get(self, req, resp):
        bearer_token = f'Bearer ' + self.call_auth_endpoint()["access_token"]
        url = "https://rihanna.atreemo.uk/api/Customer/FindCustomerDetails"
        member_number = self.get_member_number_from_query_params(req)

        payload = json.dumps({
        "SearchFilters": {
            "MemberNumber": member_number
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

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.media = json.loads(response.text)

    def get_member_number_from_query_params(self, req):
        for key, value in req.params.items():
            if key == "membernumber":
                return value            