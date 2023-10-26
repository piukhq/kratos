import json

import falcon
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from settings import settings
from amex_merchant_search import AmexMerchantSearch
from vop import VisaHelloWorld, VisaGetTransaction, VisaGetMerchant, VisaSearchMerchantGroup, VisaOfferCommunity
from givex import GivexAccountLookup, GivexAccountHistory
from stonegate import StonegateFindByEmail, StonegateFindByMemberNumber
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


class Healthz:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = "healthy"

app = falcon.App()
app.add_route("/healthz", Healthz())
app.add_route("/sgg/findByEmail", StonegateFindByEmail())
app.add_route("/sgg/findByMemberNumber", StonegateFindByMemberNumber())
app.add_route("/vop/helloworld", VisaHelloWorld())
app.add_route("/vop/gettransaction", VisaGetTransaction())
app.add_route("/vop/getmerchant", VisaGetMerchant())
app.add_route("/vop/merchantgroup", VisaSearchMerchantGroup())
app.add_route("/vop/offercommunity", VisaOfferCommunity())
app.add_route("/amex/merchantsearch", AmexMerchantSearch())
app.add_route("/givex/accountlookup", GivexAccountLookup())
app.add_route("/givex/accounthistory", GivexAccountHistory())
