import sys
import settings
import os
import subprocess
import utils
from time import sleep

while True:
    env = dict(
        COMPOSE_EMAIL=utils.env('COMPOSE_EMAIL'),
        COMPOSE_ACCOUNT_NAME=utils.env('COMPOSE_ACCOUNT_NAME'),
        COMPOSE_PASSWORD=utils.env('COMPOSE_PASSWORD'),
        DATADOG_API_KEY=utils.env('DATADOG_API_KEY'),
        DATADOG_APP_KEY=utils.env('DATADOG_APP_KEY'),
        DATADOG_TAGS=utils.env('DATADOG_TAGS', ''),
    )
    utils.init_datadog()
    utils.Report.ok()
    p = subprocess.Popen(
        ["scrapy", "runspider", "cluster_spider.py"], env=env)
    ret = p.wait()
    print("exited {}".format(ret))
    if not ret == 0:
        print("scraper failed")
        sys.exit(ret)
    sleep(settings.CHECK_INTERVAL_SECONDS)
