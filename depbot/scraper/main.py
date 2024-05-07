import json
from dataclasses import dataclass
from datetime import datetime

from .base import BaseScraper
from .utils import logger
import argparse as ap
from typing import List
from .core import *
import os


class MainScraper(BaseScraper):
    scraper_registry: dict[str, BaseScraper] = {
        "dp1": FunnyShortJokesScraper(),
        "dp2": LaughFactoryScraper(),
        "dp3": HF1Scraper(),
        "dp4": HF2Scraper(),
        "dp5": HF3Scraper(),
        "dp6": HF4Scraper(),
        "dp7": HF5Scraper(),
        "dp8": HF6Scraper(),
        "dp9": HF7Scraper(),
        "dp10": HF8Scraper(),
        "dp11": HF9Scraper(),
        "dp12": HF10Scraper(),
        "dp13": HF11Scraper(),
        "dp14": HF12Scraper(),
        "dp15": HF13Scraper(),
    }
    metadata_file = "./meta-data.json"
    metadata = {}

    def __init__(self):
        self.load_metadata()

    def scrape(self) -> None:
        return super().scrape()

    def scrape_all(self):
        logger.info("Scraping all formats")
        codes = self.scraper_registry.keys()
        self.scrape_specific(tuple(codes), force=True)

    def load_metadata(self):
        try:
            with open(self.metadata_file, "r") as f:
                self.metadata = json.load(f)
        except FileNotFoundError:
            self.metadata = {}

    def save_metadata(self):

        # Try to open the metadata file for writing
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=4)
        logger.info("Metadata saved successfully!")

    def is_scraped(self, code):
        if code not in self.metadata:
            return False
        if self.metadata.get(code, {}).get("time") is not None:
            return True

    def scrape_specific(self, scraper_codes, force):
        for code in scraper_codes:

            if code not in self.scraper_registry.keys():
                logger.warning(f"Unknown format code: {code}")
                continue

            if force or not self.is_scraped(code):
                scraper = self.scraper_registry[code]
                scraper.scrape()
                logger.info(f"Scraped {code} successfully")
                self.metadata[code] = {
                    "name": scraper.format.value,
                    "last_scraped": datetime.now().isoformat(),
                    "time": scraper.time,
                }

            else:
                logger.info(
                    f"Data for {code} is up-to-date. Use --force to scrape again."
                )
        self.save_metadata()


def main():
    parser = ap.ArgumentParser(description="Scraper Cli")

    parser.add_argument(
        "-c",
        "--codes",
        metavar="code",
        help="Format code to scrape",
        nargs="+",
        type=str,
    )

    parser.add_argument("-a", "--all", action="store_true")

    parser.add_argument("-f", "--force", action="store_true")

    args = parser.parse_args()
    print(args.all, args.codes)
    scraper = MainScraper()
    if args.all:
        scraper.scrape_all()
    elif args.codes:
        scraper.scrape_specific(args.codes, args.force)
    else:
        print("Please provide a format code or use --all to scrape all formats.")


if __name__ == "__main__":
    main()
