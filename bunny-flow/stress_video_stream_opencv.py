
import asyncio
from playwright.async_api import async_playwright, Playwright
from prefect.task_runners import ConcurrentTaskRunner
from prefect import task, flow, get_run_logger
from prefect.cache_policies import NO_CACHE
from playwright.sync_api import sync_playwright, Playwright
import os
import cv2
@task(cache_policy=NO_CACHE)
def process_video(i, url):
    cap = cv2.VideoCapture(url)
    j = 0
    res = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        
        if not ret:
            break
        folder = f"video_stream_opencv/{i}"
        file = f"video_stream_opencv/{i}/image_{j}.jpg"

        if not os.path.exists(folder):
            os.makedirs(folder)

        res.append(frame)
        cv2.imwrite(file, frame)        

        j += 1
    cap.release()
    return res

import unittest
class TestFrameEquality(unittest.TestCase):
    @task(cache_policy=NO_CACHE)
    def test_frame_equality(self, frames):
        import numpy as np
        # as both are video streams, we can compare the number of frames
        self.assertTrue(all([np.array_equal(a, b) for a, b in zip(frames, frames[1:])]))


@flow(task_runner=ConcurrentTaskRunner())
def main():
    n = 3
    final_res = []
    url = 'https://vz-f54b3be4-646.b-cdn.net/b8c08c53-03b7-4df1-a2cf-9d01b4dcf4fb/playlist.m3u8'
    prcs_video = [process_video.submit(i, url) for i in range(n)]
    [final_res.append(i.result()) for i in prcs_video if i.result()]
    TestFrameEquality().test_frame_equality(final_res)


if __name__ == '__main__':
    main()

