import falcon

from settings import settings
from amex_merchant_search import AmexMerchantSearch
from vop import VisaHelloWorld, VisaGetTransaction, VisaGetMerchant, VisaSearchMerchantGroup, VisaOfferCommunity
from givex import GivexAccountLookup, GivexAccountHistory
from stonegate import StonegateFindByEmail, StonegateFindByMemberNumber
from payment_cards import PaymentCards

from punchh import PunchhUserInfo, PunchhUserExtensiveTimeline


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
app.add_route("/v2/payment_cards/", PaymentCards())
app.add_route("/punchh/users/info", PunchhUserInfo())
app.add_route("/punchh/users/extensive_timeline", PunchhUserExtensiveTimeline())
