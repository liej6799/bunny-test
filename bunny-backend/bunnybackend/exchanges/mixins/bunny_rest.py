'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
import asyncio
from decimal import Decimal
import hashlib
import hmac
import logging
import time
from urllib.parse import urlencode


from yapic import json

from bunnybackend.defines import GET, POST, BUNNY_VIDEO_LIBRARY
from bunnybackend.exchange import RestExchange

LOG = logging.getLogger('feedhandler')

class BunnyRestMixin(RestExchange):
    api = "https://api.bunny.net/"

    def _request(self, method: str, endpoint: str, auth: bool = False, payload={}, api=None):
        query_string = urlencode(payload)
        
        if auth:
            header = {
                "accept": "application/json",
                "AccessKey": self.key_id
            }
        else:
            header = {
                "accept": "application/json"
            }
  
        if not api:
            api = self.api

        url = f'{api}{endpoint}?{query_string}'
    
        if method == GET:
            return self.http_sync.read(address=url, headers=header, isCache=True, retry_message=self.retry_message)
        elif method == POST:
            return self.http_sync.write(address=url, data=None)

    def retry_message(self):
        return
        {
            'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency.'
        }

    def refresh_video_library(self):
        return [BUNNY_VIDEO_LIBRARY]

    def get_video_library(self):
        return self._request(GET, 'videolibrary', auth=True)