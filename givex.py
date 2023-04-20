import falcon
import uuid
from jsonrpclib import jsonrpc
from givex_response_structures import Givex996Response, Givex995Response
from givex_api import load_credentials_from_vault
from settings import settings
import logging

logger = logging.getLogger(__name__)


class GivexAccountHistory:
    def on_get(self, req, resp):
        if req.query_string == f"auth={settings.givex_auth_token}":
            logger.error("On get")
            givex_username, givex_password = load_credentials_from_vault()    

            myuuid = uuid.uuid4()
            givex = jsonrpc.ServerProxy("https://%s:%s" % ("dev-dataconnect.givex.com", "50104"))
            response = givex.dc_995('en', str(myuuid), givex_username, givex_password, req.media["givex_number"],  "", "", "Points")


            response_995 = Givex995Response(response)
            resp.media = vars(response_995)
        else:
            resp.status = falcon.HTTP_401
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "Access Denied"
    

class GivexAccountLookup:
    
    def on_get(self, req, resp):
        if req.query_string == f"auth={settings.givex_auth_token}":
            logger.error("On get")
            givex_username, givex_password = load_credentials_from_vault()    

            myuuid = uuid.uuid4()
            givex = jsonrpc.ServerProxy("https://%s:%s" % ("dev-dataconnect.givex.com", "50104"))
            response = givex.dc_996('en', str(myuuid), givex_username, givex_password, req.media["givex_number"])


            response_996 = Givex996Response(response)
            resp.media = vars(response_996)
        else:
            resp.status = falcon.HTTP_401
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "Access Denied"


