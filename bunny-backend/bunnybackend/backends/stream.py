

from typing import Tuple
from bunnybackend.defines import *
from datetime import datetime as dt
from bunnybackend.config import Config
import json


class Stream():
    def __init__(self):
        NotImplemented
        # self.stream = self.stream
        # self.browser = self.browser

    async def read(self):
        
        return self._read()
     

class DemoStream(Stream):
    def _read(self):
        return [{BROWSER:MSEDGE,STREAM:BUNNY_STREAM}]
  