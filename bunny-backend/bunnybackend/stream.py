
from bunnybackend.defines import *

BUNNY_STREAM = 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8'

class Stream():
    hls_url = NotImplemented
    id = NotImplemented
    validity = NotImplemented

    def __init__(self, stream_type):
        self.stream_type = stream_type

    def get_url(self):
        return self.hls_url
    
    # def bunny_stream(self):
    #     return BunnyStream(BUNNY_STREAM, 'bunny', False, None, 'HLS', 'VALID')

    # def __getitem__(self, key):
    #     if key == BUNNY_STREAM:
    #         return self.bunny_stream

class BunnyStream(Stream):
    hls_url = 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8'
    id = BUNNY
    validity = True

class SintelStream(Stream):
    hls_url = 'https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8'
    id = SINTEL
    validity = True

#     def __getitem__(self, key):
#         if key == BUNNY_STREAM:
#             return self.bunny_stream
# STREAMS = [
#     Stream('https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8', 'sintel', False, None, 'HLS', 'VALID'),
#     Stream('https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'bunny', False, None, 'HLS', 'VALID')
#     ]

