import unittest
from cluster_spider import ClusterScraper
from responses import fake_response_from_file


class ClusterScraperTest(unittest.TestCase):
    def setUp(self):
        fake_response = fake_response_from_file('fixtures/compose.html')
        self.scraper = ClusterScraper(fake_response)

    def test_name(self):
        self.assertEqual(self.scraper.name, 'FAKEACCNAME-eu-west1-c00')

    def test_metrics(self):
        self.assertEqual(self.scraper.metrics, {
            'FAKEACCNAME-eu-west1-c00.0.compose.direct': {
                'ram': {
                    'in_use': 23.0,
                    'used': 3.59,
                    'total': 15.7,
                },
                'disk': {
                    'in_use': 8.0,
                    'used': 12.0,
                    'total': 157,
                }
            },
            'FAKEACCNAME-eu-west1-c00.1.compose.direct': {
                'ram': {
                    'in_use': 47.0,
                    'used': 7.29,
                    'total': 15.7,
                },
                'disk': {
                    'in_use': 12.0,
                    'used': 19.0,
                    'total': 157,
                }
            },
            'FAKEACCNAME-eu-west1-c00.2.compose.direct': {
                'ram': {
                    'in_use': 18.0,
                    'used': 2.86,
                    'total': 15.7,
                },
                'disk': {
                    'in_use': 6.0,
                    'used': 10.0,
                    'total': 157,
                }
            }
        })
