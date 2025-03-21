'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''

from bunnybackend.defines import *
from bunnybackend.player import Player
from playwright.sync_api import sync_playwright, Playwright
from bunnybackend.types import StreamPlay

from time import time
from yapic import json
from decimal import Decimal

class Hls(Player):
    id = HLS
    lib_url = 'https://liej6799.github.io/bunny-test/bunny-flow/script/hls/'


    def refresh_stream_play(self):
        return [HLS_STREAM_PLAY]
    
    def process_stream_play(self):
        
        self.page.goto(self.lib_url)
        self.page.locator('#url').fill(self.payload.stream.get_url())
        self.page.locator('#btn').click()

    def stream_play_test(self):
        return self.run_playwright(self.process_stream_play)

    def _stream_play_test(self, msg, ts):
        data = []
        try:
            data.append(StreamPlay(
                        library=self.id,
                        stream=(self.stream),
                        browser = (self.selected_browser),
                        iter=self.iter,
                        screenshot=self.screenshot,

                        console=(msg['console']),
                        error=(msg['error']),
                        exception=(msg['exception']),
                        
                        ))

        except Exception as a:
            print(a)
            pass
        return data

    def message_handler(self, type, msg, symbol=None):

        try:
            msg = json.loads(msg, parse_float=Decimal)
        except Exception:
            pass

        if type == HLS_STREAM_PLAY:
           return self._stream_play_test(msg, time())

    def __getitem__(self, key):
        print('getitem', key)
        if key == REFRESH_STREAM_PLAY:
            return self.refresh_stream_play
        
        elif key == HLS_STREAM_PLAY:
            return self.stream_play_test
        