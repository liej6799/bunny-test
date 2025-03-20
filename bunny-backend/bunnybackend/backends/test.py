

from typing import Tuple
from bunnybackend.browser import ChromeBrowser, FirefoxBrowser
from bunnybackend.defines import *
from datetime import datetime as dt
from bunnybackend.config import Config
import json

from bunnybackend.stream import BunnyStream, SintelStream


class Test():
    def __init__(self):
        NotImplemented
        # self.stream = self.stream
        # self.browser = self.browser

    async def read(self):
        
        return self._read()
     

class DemoTest(Test):
    def _read(self):
        return [
            {BROWSER:FirefoxBrowser(),STREAM:BunnyStream(stream_type=HLS)},
            {BROWSER:FirefoxBrowser(),STREAM:SintelStream(stream_type=HLS)},
            {BROWSER:ChromeBrowser(),STREAM:BunnyStream(stream_type=HLS)},
            {BROWSER:ChromeBrowser(),STREAM:SintelStream(stream_type=HLS)},
            ]
  