import json
from wsgiref.simple_server import make_server

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


class Healthz():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "healthy"

class VisaHelloWorld:
    def on_get(self, req, resp):
        if req.query_string == f"auth={settings.auth_token}":
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
        if req.query_string == f"auth={settings.auth_token}":
            r = self.vop_request(
                transaction_ammount=req.media["transactionAmount"],
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
        self, transaction_ammount: float, transaction_date: str, user_key: str, community_code: str
    ) -> json:
        for _ in range(10):
            try:
                r = requests.post(
                    "https://api.visa.com/vop/v1/users/gettransaction",
                    auth=(vop_auth["username"], vop_auth["password"]),
                    cert=("/tmp/vop_cert.pem", "/tmp/vop_key.pem"),
                    headers={"Content-Type": "application/json"},
                    json={
                        "transactionAmount": transaction_ammount,
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


app = falcon.App()
app.add_route("/healthz", Healthz())
app.add_route("/vop/helloworld", VisaHelloWorld())
app.add_route("/vop/gettransaction", VisaGetTransaction())
