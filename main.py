import settings
import os
import subprocess
import utils
from time import sleep

while True:
    utils.init_datadog()
    utils.Report.ok()
    subprocess.Popen(
        ["scrapy", "runspider", "cluster_spider.py"], env=os.environ)
    sleep(settings.CHECK_INTERVAL_SECONDS)
