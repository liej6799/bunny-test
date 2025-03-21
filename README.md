# bunny_test

Standardized Python Test Script for REST API and Stream Testing.

### Motivation
Allow easier implementation of new test case, with prefect backend for distributed testing across different workers.

### Supported / Implemented API / Libraries
API for Listing Video and Libraries https://docs.bunny.net/reference/bunnynet-api-overview

Stream Test for VideoJS, HLS, BunnyStream with playwright.

openCV to process the stream and dump frame is available as POC. (Uses ffmpeg as backend) [here](https://github.com/liej6799/bunny-test/blob/main/bunny-flow/stress_video_stream_opencv.py)

Postgres Database to store API Result

Integration with prefect for concurrency, logging and allow possibility for running under worker agent across different country for more detailed testing.

### To be Implemented / Current Limitations
When Testing for multiple stream, Need to have limit and process the request by batch to prevent OOM on the worker.

Add better logging analysis, current logging is only based on the console from playwright

Add more test case such as [chaos-stream-proxy](https://github.com/Eyevinn/chaos-stream-proxy) to check is the library able to recover from it and restart.


### Screenshot
![image](https://github.com/user-attachments/assets/086320af-c892-4b7a-b7b8-bb2a5cc9d93c)

Running multiple stream with playwright testing and show the output on the folder [here](https://github.com/liej6799/bunny-test/tree/main/bunny-flow/backend-folder)

### Test Result
List of Stream Test Result with logging and screenshot

https://github.com/liej6799/bunny-test/tree/main/bunny-flow/backend-folder

