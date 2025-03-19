

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
        self.page.screenshot(path='screenshot.png')
        self.browser.close()

    def run_playwright(self):
        print('run_playwright')
        import time
        with sync_playwright() as playwright:
            self.playwright = playwright
            self.init_playwright()
            
            self.process_stream_play()
            time.sleep(10)
        
            self.exit_playwright()
            return [self.console, self.error, self.exception]
        
        return []          
    
    def process_stream_play():
        raise NotImplementedError()
    
    def set_browser(self):
        if self.payload.browser == CHROME:
            self.browser = self.playwright.chromium.launch(channel="chrome", headless=True)
        elif self.payload.browser == MSEDGE:
            self.browser = self.playwright.chromium.launch(channel="msedge", headless=True)
        elif self.payload.browser == FIREFOX:
            self.browser = self.playwright.firefox.launch(headless=True)
  

    def set_page(self):
        self.page = self.browser.new_page()
        self.page.on("console", lambda msg: self.console.append(msg.text))
        self.page.on("error", lambda msg: self.error.append(msg.text))       

        self.page.goto(self.lib_url)




   
