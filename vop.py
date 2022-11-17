import json

import falcon
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from settings import settings

credential = DefaultAzureCredential()
kv_client = SecretClient(vault_url=settings.keyvault_url, credential=credential)

vop_auth = {
    "cert": json.loads(kv_client.get_secret("vop-clientCert").value)["value"],
    "key": json.loads(kv_client.get_secret("vop-clientKey").value)["value"],
    "username": json.loads(kv_client.get_secret("vop-authUserId").value)["value"],
    "password": json.loads(kv_client.get_secret("vop-authPassword").value)["value"],
}

for i in ["cert", "key"]:
    with open(f"/tmp/vop_{i}.pem", "w") as f:
        f.write(vop_auth[i])

class VisaHelloWorld:
    def on_get(self, req, resp):
        if req.query_string == f"auth={settings.visa_auth_token}":
            request = self.vop_request()
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.media = request
        else:
            resp.status = falcon.HTTP_401
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "Access Denied"

    def vop_request(self):
        for _ in range(10):
            try:
                r = requests.get(
                    "https://api.visa.com/vdp/helloworld",
                    auth=(vop_auth["username"], vop_auth["password"]),
                    cert=("/tmp/vop_cert.pem", "/tmp/vop_key.pem"),
                    headers={"Content-Type": "application/json"},
                )
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                print("retrying request")
                continue
            break
        return r.json()


class VisaGetTransaction:
    def on_post(self, req, resp):
        if req.query_string == f"auth={settings.visa_auth_token}":
            r = self.vop_request(
                transaction_amount=req.media["transactionAmount"],
                transaction_date=req.media["transactionDate"],
                user_key=req.media["userKey"],
                community_code=req.media["communityCode"],
            )
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.media = r
        else:
            resp.status = falcon.HTTP_401
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "Access Denied"

    def vop_request(
        self, transaction_amount: float, transaction_date: str, user_key: str, community_code: str
    ) -> json:
        for _ in range(10):
            try:
                r = requests.post(
                    "https://api.visa.com/vop/v1/users/gettransaction",
                    auth=(vop_auth["username"], vop_auth["password"]),
                    cert=("/tmp/vop_cert.pem", "/tmp/vop_key.pem"),
                    headers={"Content-Type": "application/json"},
                    json={
                        "transactionAmount": transaction_amount,
                        "transactionDate": transaction_date,
                        "userKey": user_key,
                        "communityCode": community_code,
                    },
                )
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                continue
            break
        return r.json()

class VisaSearchMerchantGroup:
    def on_get(self, req, resp):
        if req.query_string == f"auth={settings.visa_auth_token}":
            r = self.vop_request(
                community_code=settings.visa_community_code
            )
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.media = r
        else:
            resp.status = falcon.HTTP_401
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "Access Denied"        

    def vop_request(self, community_code):
        for _ in range(10):
            try:
                r = requests.get(
                    f"https://sandbox.api.visa.com/vop/v1/merchants/groups?communityCode={community_code}",
                    auth=(vop_auth["username"], vop_auth["password"]),
                    cert=("/tmp/vop_cert.pem", "/tmp/vop_key.pem"),
                    headers={"Content-Type": "application/json"},
                )
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                print("retrying request")
                continue
            break
        return r.json()


class VisaGetMerchant:
    def on_get(self, req, resp):
        if req.query_string == f"auth={settings.visa_auth_token}":
            r = self.vop_request(
                community_code=req.media["communityCode"],
                merchant_name=req.media["merchantName"],
                merchant_country_code=req.media["merchantCountryCode"],
                merchant_postal_code=req.media["merchantPostalCode"],
            )
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.media = r
        else:
            resp.status = falcon.HTTP_401
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "Access Denied"

    def vop_request(
        self, community_code: str, merchant_name: str, merchant_country_code: int, merchant_postal_code: str
    ):

        for _ in range(10):
            try:
                r = requests.get(
                    f"https://api.visa.com/vop/v1/merchants/search/details",
                    auth=(vop_auth["username"], vop_auth["password"]),
                    cert=("/tmp/vop_cert.pem", "/tmp/vop_key.pem"),
                    headers={"Content-Type": "application/json"},
                    params={
                        "communityCode": community_code,
                        "merchantName": merchant_name,
                        "merchantCountryCode": merchant_country_code,
                        "merchantPostalCode": merchant_postal_code,
                    }
                )
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                print("retrying request")
                continue
            break
        return r.json()
