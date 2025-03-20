

from bunnybackend.config import Config
from bunnybackend.connection import HTTPSync
from bunnybackend.exceptions import UnsupportedSymbol



class Exchange:
    id = NotImplemented
    websocket_endpoints = NotImplemented
    rest_endpoints = NotImplemented
    _parse_symbol_data = NotImplemented
    websocket_channels = NotImplemented
    rest_channels = NotImplemented
    request_limit = NotImplemented
    valid_candle_intervals = NotImplemented
    candle_interval_map = NotImplemented
    flow_id = NotImplemented
    flow_name = NotImplemented
    payload = NotImplemented
    http_sync = HTTPSync()
    
    def __init__(self, config=None, sandbox=False, flow=None, payload=None, subaccount=None, symbols=None, **kwargs):
        self.config = Config(config=config)
        self.sandbox = sandbox
        self.subaccount = subaccount

        keys = self.config[self.id.lower(
        )] if self.subaccount is None else self.config[self.id.lower()][self.subaccount]
        self.key_id = keys.key_id
        self.key_secret = keys.key_secret
        self.key_passphrase = keys.key_passphrase
        self.account_name = keys.account_name
        self.flow_id= flow['flow_id']
        self.flow_name= flow['flow_name']
        
        self.payload = payload
        

        
        # self.flow_id = if flow is None else flow.flow_id 
        # self.flow_name = flow_name

        self.ignore_invalid_instruments = self.config.ignore_invalid_instruments


   
class RestExchange:
    def refresh_symbol_lookup(self):
        raise NotImplementedError
