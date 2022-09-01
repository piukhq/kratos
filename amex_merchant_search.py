import logging
import falcon
from settings import settings
from amex_api import search_amex_merchants

logger = logging.getLogger(__name__)

class AmexMerchantSearch:

    def on_post(self, req, resp):
        if req.query_string == f"auth={settings.amex_auth_token}":

            request_body = {
                        "partner_id": "AADP0050",
                        "postalCode": req.media["postalCode"],
                        "merchantName": req.media["merchantName"],
                        "street": req.media["street"],
                        "city": req.media["city"],
                        "state": req.media["state"]
            }
            r = search_amex_merchants(request_body)
            resp.media = r.json()
        else:
            resp.status = falcon.HTTP_401
            resp.content_type = falcon.MEDIA_TEXT
            resp.text = "Access Denied"