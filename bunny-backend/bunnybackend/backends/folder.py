

from typing import Tuple
from bunnybackend.defines import *
from datetime import datetime as dt
from bunnybackend.config import Config
import json


class Folder():
    id = FOLDER  
    def __init__(self, config=None):
        if config is None:
            config = 'config.yaml'

        self.config = Config(config=config)
        keys = self.config[self.id.lower()]
        self.base_folder = keys.path


    async def write(self, updates: list):
       
        return self._write(updates)
     

class ScreenshotFolder(Folder):
    def _write(self, args):
        from pathlib import Path
        import io
        import os
        from PIL import Image

        for i in args:
            self.folder = os.path.join(self.base_folder, i.library + '-' + i.stream.id + '-' + i.browser.id)
            Path(self.folder).mkdir(parents=True, exist_ok=True)
            file = os.path.join(self.folder, 'screenshot' + '-' + str(i.iter) + '.png')
            image = Image.open(io.BytesIO(i.screenshot))
            image.save(file)  # Specify the desired output file name  

       
class LogFolder(Folder):
    def _write(self, args):
        from pathlib import Path
        import io
        import os
        from PIL import Image
        import jsonpickle
     
        for i in args:
            
            self.folder = os.path.join(self.base_folder, i.library + '-' + i.stream.id + '-' + i.browser.id)
            Path(self.folder).mkdir(parents=True, exist_ok=True)
            file = os.path.join(self.folder, 'log' + '-' + str(i.iter) + '.txt')
            with open(file, 'w') as json_file:
                json_file.write(jsonpickle.encode(i))
         