import sys
import subprocess
import utils
from time import sleep
import scrapy
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from twisted.internet import task
from scrapy.crawler import CrawlerRunner
from cluster_spider import ClusterSpider

def crawl(settings=None):
    runner = CrawlerRunner(settings=settings)
    runner.crawl(ClusterSpider)
    runner.join()

def main():
    """configure and start crawler"""
    settings = dict(
        COMPOSE_EMAIL=utils.env('COMPOSE_EMAIL'),
        COMPOSE_ACCOUNT_NAME=utils.env('COMPOSE_ACCOUNT_NAME'),
        COMPOSE_PASSWORD=utils.env('COMPOSE_PASSWORD'),
        COMPOSE_CLUSTER_ID=utils.env('COMPOSE_CLUSTER_ID'),
        DATADOG_API_KEY=utils.env('DATADOG_API_KEY'),
        DATADOG_APP_KEY=utils.env('DATADOG_APP_KEY'),
        DATADOG_TAGS=utils.env('DATADOG_TAGS', ''),
        USER_AGENT='Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        ROBOTSTXT_OBEY=True,
        LOG_LEVEL=utils.env('LOG_LEVEL', 'WARNING'),
        CHECK_INTERVAL_SECONDS=int(utils.env('CHECK_INTERVAL_SECONDS', 600)),
    )
    configure_logging(settings)
    loop = task.LoopingCall(crawl, settings=settings)
    loop.start(settings.get('CHECK_INTERVAL_SECONDS'))
    reactor.run()

if __name__ == "__main__":
    main()
