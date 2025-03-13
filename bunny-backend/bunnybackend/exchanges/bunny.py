'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''

from bunnybackend.defines import *
from bunnybackend.exchange import Exchange
from bunnybackend.connection import RestEndpoint, Routes
from bunnybackend.exchanges.mixins.bunny_rest import BunnyRestMixin
from bunnybackend.exceptions import UnsupportedSymbol
from time import strftime, localtime

from typing import Dict, List, Tuple, Union
from decimal import Decimal
import csv
from time import time
from yapic import json
from bunnybackend.types import RefreshVideoLibrary
from prefect import flow, task


class Bunny(Exchange, BunnyRestMixin):
    id = BUNNY
    rest_endpoints = [RestEndpoint(
        'https://api.bunny.net/', routes=Routes(['query?function=LISTING_STATUS']))]
    key_seperator = ','


    def _get_video_library(self, msg, ts):
        data = []

        for i in msg:
            try:
                data.append(RefreshVideoLibrary(
                            id=(i['Id']),
                            name=(i['Name']),
                            video_count=(i['VideoCount']),
                            traffic_usage=(i['TrafficUsage']),

                            storage_usage=(i['StorageUsage']),
                            date_created=(i['DateCreated']),

                            timestamp=ts,
                            raw=i
                            ))
      

            except Exception:
                pass
            
        return data

    def message_handler(self, type, msg, symbol=None):

        try:
            msg = json.loads(msg, parse_float=Decimal)
        except Exception:
            pass

        if type == BUNNY_VIDEO_LIBRARY:
           return self._get_video_library(msg, time())
      
        
    def __getitem__(self, key):
        if key == REFRESH_VIDEO_LIBRARY:
            return self.refresh_video_library
        elif key == BUNNY_VIDEO_LIBRARY:
            return self.get_video_library
            
        
        
       
