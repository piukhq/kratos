import random
import time
from settings import settings

class Amex_Connection:
    def __init__(self, input_client_key, input_client_secret):
        self.timestamp=int(round(time.time() * 1000))
        self.httpMethod = 'POST'
        self.nonce = (''.join([str(random.randint(0,9)) for i in range(9)])) + "AMEX"  
        self.resourceURI = '/marketing/v4/smartoffers/merchant/inquiry_results'
        self.hostname=settings.amex_hostname
        self.port="443"
        self.client_key = input_client_key
        self.client_secret = input_client_secret
        self.messageId = int(round(time.time() * 1000)) 
