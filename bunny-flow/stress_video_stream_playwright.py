import asyncio
from playwright.async_api import async_playwright, Playwright
from prefect.task_runners import ConcurrentTaskRunner
from prefect import task, flow, get_run_logger
from prefect.cache_policies import NO_CACHE
from playwright.sync_api import sync_playwright, Playwright

@task(cache_policy=NO_CACHE)
def run(i):
    import time
    with sync_playwright() as playwright:
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = chromium.launch()
        page = browser.new_page()
        page.goto('https://storage.bunnycdn.com/test-st/tears_of_steel_1080p.webm?accessKey=5efa6332-74ea-47da-8a3f39020dff-0281-4d1b')
        time.sleep(60)
        # other actions...
        page.screenshot(path='video_stream_playwright/screenshot' + str(i) + '.png')
        
        browser.close()

@flow(task_runner=ConcurrentTaskRunner())
def main():
    for i in range(10):
        run.submit(i)

        

if __name__ == '__main__':
    main()

