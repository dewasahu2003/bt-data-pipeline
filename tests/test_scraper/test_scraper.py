import unittest
from unittest.mock import patch, MagicMock
from scraper.base import BaseScraper
from scraper.core import HF1Scraper, HF2Scraper


class TestScrapers(unittest.TestCase):

    def setUp(self):
        # Initialize instances of all scrapers
        self.scrapers = [
            HF1Scraper(),
            HF2Scraper(),
            # Add instances of other scrapers here
        ]

    def tearDown(self):
        # Clean up instances of scrapers
        for scraper in self.scrapers:
            del scraper

    def test_scrape_methods(self):
        for scraper in self.scrapers:
            scraper: BaseScraper
            # Mocking dependencies
            with patch("my_package.scraper.load_dataset") as mock_load_dataset:
                mock_df = MagicMock()
                mock_load_dataset.return_value = {"train": mock_df}
                mock_df.to_pandas.return_value = mock_df
                mock_df["text"].to_pandas.return_value = [
                    "Mocked text 1",
                    "Mocked text 2",
                ]

                # Call the scrape method for the current scraper
                scraper.scrape()

                # Add assertions to test other aspects of the scrape method for each scraper


if __name__ == "__main__":
    unittest.main()
