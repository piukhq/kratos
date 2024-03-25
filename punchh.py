import falcon
from settings import settings
import logging
import hmac
import json
from urllib.parse import urlencode, urljoin
from azure.core.exceptions import ServiceRequestError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests
from common_modules import hash_ids
import hashlib


credential = DefaultAzureCredential()
kv_client = SecretClient(vault_url=settings.keyvault_url, credential=credential)

def generate_signature(punchh_uri: str, request_body: dict, secret: str) -> str:
    payload = ''.join((punchh_uri,(request_body)))        
    secret = get_mobile_api_secret()
    signature = hmac.new(bytes(secret, 'UTF-8'), bytes(payload, 'UTF-8'), hashlib.sha256).hexdigest()
    return signature

def generate_punchh_app_device_id(user_id) -> str:
    return hash_ids.encode(user_id)


def get_user_id_from_query_parameters(req):
    for key, value in req.params.items():
        if key == "user_id":
            return value

def get_mobile_api_secret():
    secret = kv_client.get_secret("tgi-fridays-secret").value
    return secret

def get_platform_api_secret():
    secret = kv_client.get_secret("tgi-fridays-admin-key").value
    return secret        

def get_platform_api_headers():
    response = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f'Bearer {get_platform_api_secret()}'
        }
    return response

def get_mobile_api_headers(uri, payload):
    response = {
            "Content-Type": "application/json",
            "User-Agent": "bink",
            "punchh-app-device-id": generate_punchh_app_device_id(payload["user"]["email"]),
#            "x-pch-digest": signature
            "x-pch-digest": generate_signature(uri, json.dumps(payload), get_mobile_api_secret()),
        }
    return response

class PunchhUserInfo:
    def on_get(self, req, resp):
        punchh_url = settings.punchh_dashboard_api_url
        user_id = get_user_id_from_query_parameters(req)

        punchh_payload = json.dumps({
            "user_id": user_id
        })

        punchh_uri = "/api2/dashboard/users/info"
        headers = get_platform_api_headers()
        response = requests.request("GET", urljoin(punchh_url, punchh_uri), headers=headers, data=punchh_payload)

        resp.status = response.status_code
        resp.content_type = falcon.MEDIA_JSON
        resp.media = json.loads(response.text)

class PunchhUserExtensiveTimeline:
    def on_get(self, req, resp):
        punchh_url = settings.punchh_dashboard_api_url
        user_id = get_user_id_from_query_parameters(req)
        punchh_uri = f'/api2/dashboard/users/extensive_timeline?user_id={user_id}'
        headers = get_platform_api_headers()
        response = requests.request("GET", urljoin(punchh_url, punchh_uri), headers=headers)

        logging.error(f'>>> {response.text}')

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.media = json.loads(response.text)

class PunchhDashboardLocations:
    def on_get(self, req, resp):
        punchh_url = settings.punchh_dashboard_api_url
        punchh_uri = "/api2/dashboard/locations"
        headers = get_platform_api_headers()
        response = requests.request("GET", urljoin(punchh_url, punchh_uri), headers=headers)


        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.media = json.loads(response.text)

class PunchhUserLogin:
    def on_post(self, req, resp):
        punchh_url = settings.punchh_mobile_api_url
        punchh_uri = "/api2/mobile/users/login"
        request_body = json.dumps(req.media)
        headers = get_mobile_api_headers(punchh_uri, req.media)
        response = requests.request("GET", urljoin(punchh_url, punchh_uri), headers=headers, data=request_body)


        resp.status = response.status_code
        resp.content_type = falcon.MEDIA_JSON
        try: 
            resp.media = json.loads(response.text)
            logging.error(f'>>> {resp.media}')
        except json.decoder.JSONDecodeError:
            logging.error(resp.status)
            logging.error(f' Error in JSON payload: {response.text[0:100]}')
            resp.media = response.text