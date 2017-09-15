# Compose cluster metrics scraper

A scraper for the webpage of our Compose cluster, logging metrics to Datadog. An app in `main.py` runs this scraper at regular intervals. This app is then deployed on the GOV.UK PaaS.

## How to run

Use Python 3. Install pip packages with `pip3 install -r requirements.txt`.

You can run the app with `python3 main.py` but will need to provide several environment variables:

* `DATADOG_API_KEY` and `DATADOG_APP_KEY`: Datadog API credentials sufficient to log metrics
* `COMPOSE_EMAIL` and `COMPOSE_PASSWORD`: Compose login details able to view the cluster
* `COMPOSE_ACCOUNT_NAME`: Compose account name
* `COMPOSE_CLUSTER_ID`: Id of the cluster to query

## How to work on the scraper

`python3 -m unittest test_cluster_scraper` runs the scraper against a HTML file. It does not log to Datadog and does not require the above credentials.

If Datadog alerting tells you the scraper is no longer functioning, the suggested path is:

1. Manually update the `responses/fixtures/compose.html` HTML file and the test expectations;
2. Alter the scraper until those tests pass;
3. Run the app locally and ensure it is reporting correctly to Datadog.
4. Have your changes reviewed and manually create a new tagged release once they are merged.
