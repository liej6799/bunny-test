import asyncio
import playwright
from playwright.async_api import async_playwright, Playwright
from prefect.task_runners import ConcurrentTaskRunner
from prefect import tags, task, flow, get_run_logger
from prefect.cache_policies import NO_CACHE
from playwright.sync_api import sync_playwright, Playwright
import time

def play_video(page, stream):

    page.locator('#url').fill(stream.url)
    page.locator('#btn').click()

