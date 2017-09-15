import scrapy
import utils
import re
from datetime import datetime, timedelta
from scrapy.http import Request
from datadog import api


class ClusterSpider(scrapy.Spider):
    utils.init_datadog()

    name = 'cluster'
    allowed_domains = ['app.compose.io']
    start_urls = ['https://app.compose.io/session/new']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formxpath='//form[@class="login-form"]',
            formdata={
                'user[email]': utils.env('COMPOSE_EMAIL'),
                'user[password]': utils.env('COMPOSE_PASSWORD'),
            },
            callback=self.after_login)

    def after_login(self, response):
        url = 'https://app.compose.io/{}/clusters/{}'.format(utils.env('COMPOSE_ACCOUNT_NAME'), utils.env('COMPOSE_CLUSTER_ID'))
        yield Request(url=url, callback=self.action)

    def action(self, response):
        try:
            scraped_cluster = ClusterScraper(response)
        except Exception as e:
            utils.Report.critical(
                'Could not obtain cluster name! {}'.format(e))
            return

        # Save the metrics to Datadog
        for host_name, host_metrics in scraped_cluster.metrics.items():
            for resource_name, resource_metrics in host_metrics.items():
                for name, value in resource_metrics.items():
                    metric_name = 'compose.cluster.host.{}.{}'.format(
                        resource_name, name)
                    metric_unit = ClusterScraper.UNITS_FROM_NAME[name]
                    utils.send_metric(
                        metric_name=metric_name,
                        metric_description=metric_name + ' description',
                        metric_unit=metric_unit,
                        metric_value=value,
                        cluster_name=scraped_cluster.name,
                        host_name=host_name)

        yield dict(
            cluster_name=scraped_cluster.name,
            cluster_metrics=scraped_cluster.metrics)


class ClusterScraper:
    UNITS_FROM_NAME = dict(in_use='percent', used='gibibyte', total='gibibyte')

    def __init__(self, response):
        self.name = self._cluster_name(response)
        self.metrics = self._cluster_metrics(response)

    def _cluster_name(self, response):
        return response.css('h1 .align-middle::text').extract_first().strip()

    def _cluster_metrics(self, response):
        cluster_stats = {}
        for row in response.css('table.box-table > tbody > tr'):
            try:
                scraped_host = HostScraper(row)
                cluster_stats[scraped_host.name] = scraped_host.metrics
            except Exception as e:
                utils.Report.warning('Could not scrape a host! {}'.format(e))
        return cluster_stats


class HostScraper:
    def __init__(self, row):
        self.name = self._host_name(row)
        self.metrics = self._host_metrics(row)

    def _host_name(self, row):
        return row.css('.host-status a::text').extract_first().strip()

    def _host_metrics(self, row):
        host_metrics = {}

        progress_bar_labels = row.css('.progress-bar-label::text').extract()
        for i in range(0, len(progress_bar_labels), 2):
            label_text = progress_bar_labels[i].strip()
            if label_text not in ['RAM:', 'Disk:']:
                continue
            next_label_text = progress_bar_labels[i + 1].strip()
            resource_name = label_text[:-1].lower()
            try:
                host_metrics[resource_name] = self._resource_metrics(
                    next_label_text)
            except Exception as e:
                utils.Report.warning(
                    'Could not obtain any {} metrics for host {}! {}'.format(
                        resource_name, self.name, e))
        return host_metrics

    def _resource_metrics(self, resource_metrics_text):
        """
        Extract the numbers from '18% - 2.86GB / 15.7GB'.
        """
        float_regex = r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'
        resource_metrics_regex = r'({})\% - ({})GB / ({})GB'.format(float_regex, float_regex, float_regex)
        match = re.search(resource_metrics_regex, resource_metrics_text)
        if not match:
            raise ValueError('Could not parse the metrics string of a resource.')

        metrics = {'in_use': float(match.group(1)),
                   'used': float(match.group(2)),
                   'total': float(match.group(3))}
        return metrics
