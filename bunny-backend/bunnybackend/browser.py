
from bunnybackend.defines import *


class Browser():
    id = NotImplemented

    def get_browser():
        return [id]

class FirefoxBrowser(Browser):
    id = FIREFOX

class MSEdgeBrowser(Browser):
    id = MSEDGE

class ChromeBrowser(Browser):
    id = CHROME