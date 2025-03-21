import asyncio
import playwright
from playwright.async_api import async_playwright, Playwright
from prefect.task_runners import ConcurrentTaskRunner
from prefect import tags, task, flow, get_run_logger
from prefect.cache_policies import NO_CACHE
from playwright.sync_api import sync_playwright, Playwright
import time

class Library():
    def __init__(self, name, url, version, source):
        self.name = name
        self.version = version
        self.url = url
        self.source = source
        self.folder = 'script/' + name + '-' + version

    def __str__(self):
        return f"Library(name={self.name}, url={self.url}, version={self.version}, source={self.source})"

        pass
class Stream():
    def __init__(self, url, name, chaos_enabled, chaos_type, stream_type, validity):
        self.url = url
        self.name = name
        self.chaos_enabled = chaos_enabled
        self.chaos_type = chaos_type
        self.stream_type = stream_type
        self.validity = validity

    def __str__(self):
        return f"Stream(url={self.url}, name={self.name}, chaos_enabled={self.chaos_enabled}, chaos_type={self.chaos_type}, stream_type={self.stream_type}, validity={self.validity})"


class TestResult():
    def __init__(self, console, error, exception, screenshot, test_name, test_description):
      
        self.console = console
        self.error = error
        self.exception = exception
        self.screenshot = screenshot
        self.test_name = test_name
        self.test_description = test_description      
        self.timestamp_start = None
        self.timestamp_end = None  

    def __str__(self):
        return f"TestResult(console={self.console}, error={self.error}, exception={self.exception}, screenshot={self.screenshot}, test_name={self.test_name}, test_description={self.test_description}, timestamp_start={self.timestamp_start}, timestamp_end={self.timestamp_end})"

BROWSER_LIST=['chrome','msedge','firefox']
LIBS = [
Library('video.js', 'https://liej6799.github.io/bunny-test/bunny-flow/script/videojs/', '5.10.2', 'https://codepen.io/wgenial/pen/pRRjoY')
]

STREAMS = [
    Stream('https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8', 'sintel', False, None, 'HLS', 'VALID'),
    Stream('https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8', 'bunny', False, None, 'HLS', 'VALID')
    ]


@task()
def run(browser, lib, stream, n):
    import time
    import os
    with sync_playwright() as playwright:
        console = list()
        error = list()
        exception = list()
        folder = lib.folder + '-' + browser + '-' + stream.name
        try:
            print('BROWSER', browser, lib, stream, n)
            if browser == 'chrome':
                selected_browser = playwright.chromium.launch(channel="chrome", headless=True)
            elif browser == 'msedge':
                selected_browser = playwright.chromium.launch(channel="msedge", headless=True)
            elif browser == 'firefox':
                selected_browser = playwright.firefox.launch(headless=True)
                                
            page = selected_browser.new_page()

            page.on("console", lambda msg: console.append(msg.text))
            page.on("error", lambda msg: error.append(msg.text))

            page.goto(lib.url)
            
            page.locator('#url').fill(stream.url)
            page.locator('#btn').click()

            time.sleep(10)
            # other actions...
            # Get the next console log
            print(console)

            page.screenshot(path= folder + '/screenshot' + str(n) + '.png')
            
            browser, lib, console, error, exception
  
            selected_browser.close()

        except Exception as ex:
            exception.append(ex)

        f = open(folder + "/log" + str(n) + '.txt', "a")
        f.write(str(browser))
        f.write(str(lib))
        f.write(str(console))
        f.write(str(error))
        f.write(str(exception))
        f.close()                  
        print('Task Print: ', browser, lib, console, error, exception)
        return [console, error, exception]

@task()
def process(res):
    print(res)

@flow(task_runner=ConcurrentTaskRunner())
def process_batch(batch):
    return [run.submit(task) for task in batch]
    results = []
    for run_task in run_tasks:
        results.append(run_task.result())
    return results


@flow(task_runner=ConcurrentTaskRunner())
def main():
    tasks = []
    browsers = ['firefox', 'chrome']

    for browser in browsers:
        for lib in LIBS:
            for stream in STREAMS:
                for n in range(3):
                    tasks.append((browser, lib, stream, n))

    # Process tasks in batches of 4
    batch_size = 3
    all_results = []    
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1}: {batch}")
        batch_results = process_batch(batch)
        all_results.extend(batch_results)

    # Final processing of all results
    process.submit(all_results)

   


if __name__ == '__main__':
    main()
