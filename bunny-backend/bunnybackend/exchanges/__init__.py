'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
from bunnybackend.defines import *

from .bunny import Bunny
from .common import Common
from .videojs import VideoJS
from .hls import Hls
# Maps string name to class name for use with config
EXCHANGE_MAP = {
    BUNNY: Bunny,
    COMMON: Common,
    VIDEOJS: VideoJS,
    HLS: Hls
}
