

from bunnybackend.config import Config
from bunnybackend.connection import HTTPSync
from bunnybackend.exceptions import UnsupportedSymbol
from bunnybackend.exchange import Exchange
from bunnybackend.defines import *

from playwright.sync_api import sync_playwright


class Player(Exchange):

        
    def init_playwright(self):
        self.set_browser()
        self.set_page()
        
        self.console = list()
        self.error = list()
        self.exception = list()
    
    def exit_playwright(self):
        self.iter = self.payload.iter
        self.stream = self.payload.stream
        self.selected_browser = self.payload.browser

        self.screenshot = self.page.screenshot()
        self.browser.close()

    def run_playwright(self, process):
        import time
        with sync_playwright() as playwright:
            self.playwright = playwright
            self.init_playwright()
            
            process()
            time.sleep(10)
        
            self.exit_playwright()
            return {'console':self.console, 'error':self.error, 'exception':self.exception}
        
        return []          

    def set_browser(self):
        if self.payload.browser.id == CHROME:
            self.browser = self.playwright.chromium.launch(channel="chrome", headless=True)
        elif self.payload.browser.id == MSEDGE:
            self.browser = self.playwright.chromium.launch(channel="msedge", headless=True)
        elif self.payload.browser.id == FIREFOX:
            self.browser = self.playwright.firefox.launch(headless=True)
  

    def set_page(self):
        self.page = self.browser.new_page()
        self.page.on("console", lambda msg: self.console.append(msg.text))
        self.page.on("error", lambda msg: self.error.append(msg.text))       

        self.page.goto(self.lib_url)




   
