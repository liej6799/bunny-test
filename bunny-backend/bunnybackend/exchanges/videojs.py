'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''

from bunnybackend.defines import *
from bunnybackend.player import Player
from playwright.sync_api import sync_playwright, Playwright

class VideoJS(Player):
    id = VIDEOJS
    lib_url = 'https://liej6799.github.io/bunny-test/bunny-flow/script/videojs/'

    def refresh_video_library(self):
        return [VIDEOJS_STREAM_PLAY]
    
    def process_stream_play(self):
        self.page.locator('#url').fill(self.payload.stream)
        self.page.locator('#btn').click()

    def stream_play_test(self):
        self.run_playwright()
        print('stream_play_test')

    def message_handler(self, type, msg, symbol=None):
        return []

        # if type == BUNNY_VIDEO_LIBRARY:
        #    return self._get_video_library(msg, time())
   
        # elif type == BUNNY_VIDEO:
        #    return self._get_video(msg, time())   
        
        # elif type == BUNNY_VIDEO_STREAM:
        #    return self._get_video_stream(msg, time())   
               
    def __getitem__(self, key):
        print('getitem', key)
        if key == REFRESH_STREAM_PLAY:
            return self.refresh_video_library
        
        elif key == VIDEOJS_STREAM_PLAY:
            return self.run_playwright
        