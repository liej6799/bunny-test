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

from bunnybackend.defines import BUNNY_VIDEO, BUNNY_VIDEO_STREAM, GET, POST, BUNNY_VIDEO_LIBRARY, VIDEO
from bunnybackend.exchange import RestExchange

LOG = logging.getLogger('feedhandler')

class BunnyRestMixin(RestExchange):
    api = "https://api.bunny.net/"

    def _request(self, method: str, endpoint: str, auth: bool = False, payload={}, api=None):
        query_string = urlencode(payload)
        
        if auth:
            if 'api_key' in self.payload:
                 header = {
                    "accept": "application/json",
                    "AccessKey": self.payload['api_key']
                 }
            else:                    
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
            return self.http_sync.read(address=url, headers=header, isCache=False, retry_message=self.retry_message)
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

    def refresh_video(self):
        return [BUNNY_VIDEO]

    def get_video(self):
        self.api = "https://video.bunnycdn.com/"
        library_id = self.payload['library_id']
        return self._request(GET, f'library/{library_id}/videos', auth=True)

    def refresh_video_stream(self):
        return [BUNNY_VIDEO_STREAM]
            
    def get_video_stream(self):
        self.api = "https://video.bunnycdn.com/"
        library_id = self.payload['library_id']
        video_id = self.payload['video_id']

        return self._request(GET, f'library/{library_id}/videos/{video_id}/play', auth=True)    
    