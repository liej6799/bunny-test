

from typing import Tuple
from bunnybackend.defines import *
from datetime import datetime as dt
from bunnybackend.config import Config
import json


class Folder():
    def __init__(self):
        NotImplemented
        # self.stream = self.stream
        # self.browser = self.browser

    async def write(self):
        
        return self._write()
     

class ScreenshotFolder(Folder):
    def _write(self):
        
        return [{BROWSER:MSEDGE,STREAM:BUNNY_STREAM}]
  