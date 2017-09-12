# Compose deployments scraper

Scraper for compose deployments page

`pip install -r requirements.txt`

Download the html of the compose deployments page into a directory, and run

`python -m SimpleHTTPServer 8001` within this directory

Then run the crawler with

`scrapy crawl deployment`

the css selectors are very basic and would need to be refined. Its also only
outputting the rows we are interested in at the moment, need to break this down
further
