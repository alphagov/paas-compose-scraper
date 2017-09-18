import os
import sys
import time
from datadog import initialize, api
from datadog.api.constants import CheckStatus
from datetime import datetime, date, timedelta
from datetime import time as datetime_time


def try_parse_float(item):
    """
    Parse a string, as a float.
    :param item:
    :return:
    """
    try:
        return float(item)
    except ValueError:
        return None


def init_datadog():
    """
    Initialise the datadog instance.
    :return:
    """
    initialize(api_key=env('DATADOG_API_KEY'),app_key=env('DATADOG_APP_KEY'))


def send_metric(metric_name, metric_description, metric_unit, metric_value,
                cluster_name, host_name):
    """
    Send a new metric to Datadog.
    """
    tags = [
        'cluster:{}'.format(cluster_name),
        'host:{}'.format(host_name),
    ] + os.environ.get('DATADOG_TAGS','').split(',')
    timestamp = int(time.time())

    api.Metric.send(
        metric=metric_name,
        tags=tags,
        host=host_name,
        points=(timestamp, metric_value))

    print("sending metric: {} {} {}".format(metric_name, tags, metric_value))

    api.Metadata.update(
        metric_name=metric_name,
        description=metric_description,
        type='gauge',
        unit=metric_unit)


def report_health(status, message):
    """
    Send a custom check to the Datadog, defining the app is still up and running.
    :return:
    """
    init_datadog()

    print(message)

    check = 'compose.scraper.ok'
    tags = os.environ.get('DATADOG_TAGS', '').split(',')

    api.ServiceCheck.check(
        check=check, status=status, message=message, tags=tags)


class Report(object):
    @staticmethod
    def critical(message="Critical"):
        report_health(CheckStatus.CRITICAL, message)

    @staticmethod
    def ok(message="OK"):
        report_health(CheckStatus.OK, message)

    @staticmethod
    def warning(message="Warning"):
        report_health(CheckStatus.WARNING, message)

def env(name, default=None):
    try:
        return os.environ[name]
    except KeyError:
        if default is not None:
            return default
        print("Required environment variable '{}' not set".format(name))
        sys.exit(1)
