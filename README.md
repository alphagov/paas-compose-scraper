# Compose cluster metrics scraper

A scraper for the webpage of our Compose cluster, logging metrics to Datadog. An app in `main.py` runs this scraper at regular intervals. This app is then deployed on the GOV.UK PaaS.

## How to run

Use Python 3. Install pip packages with `pip3 install -r requirements.txt`.

You can run the app with `python3 main.py` but will need to provide several environment variables:

* `DATADOG_API_KEY`: Datadog account api key
* `DATADOG_APP_KEY`: Datadog application key
* `DATADOG_TAGS`: [OPTIONAL] Comma seperated list of tags to mark the metrics with (ie: `deployment:prod,host:metrics`
* `COMPOSE_EMAIL`: Compose account login with suitable access
* `COMPOSE_PASSWORD`: Compose password for above
* `COMPOSE_ACCOUNT_NAME`: Compose account name
* `COMPOSE_CLUSTER_ID`: Id of the cluster to query
* `CHECK_INTERVAL_SECONDS`: [OPTIONAL] number of seconds between scraping attempts (default=600)

## How to work on the scraper

`python3 -m unittest test_cluster_scraper` runs the scraper against a HTML file. It does not log to Datadog and does not require the above credentials.

If Datadog alerting tells you the scraper is no longer functioning, the suggested path is:

1. Manually update the `responses/fixtures/compose.html` HTML file and the test expectations;
2. Alter the scraper until those tests pass;
3. Run the app locally and ensure it is reporting correctly to Datadog.
4. Have your changes reviewed and manually create a new tagged release once they are merged.
