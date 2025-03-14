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
from bunnybackend.types import Flow
from prefect import flow, task


class Common(Exchange):
    id = COMMON

    def start_flow(self):
        return [START_FLOW]

    def end_flow(self):
        return [END_FLOW]
    

    def _start_flow(self, msg, ts):
        data = []
        for i in msg:
            try:
                data.append(Flow(
                    flow_id=self.flow_id,
                    flow_name=self.flow_name,
                    status=START_FLOW,
                    timestamp=ts))
    
            except Exception as a:
                print(a)
                pass
        
        return data    
        
    def _end_flow(self, msg, ts):
        data = []
        for i in msg:
            try:
                data.append(Flow(
                    flow_id=self.flow_id,
                    flow_name=self.flow_name,
                    status=END_FLOW,
                    timestamp=ts))
    
            except Exception as a:
                print(a)
                pass
        
        return data        

    def message_handler(self, type, msg):

        if type == START_FLOW:
           return self._start_flow(msg, time())
      
        elif type == END_FLOW:
           return self._end_flow(msg, time())
        
    def __getitem__(self, key):
        if key == START_FLOW:
            return self.start_flow
        elif key == END_FLOW:
            return self.end_flow
            
        
        
       
