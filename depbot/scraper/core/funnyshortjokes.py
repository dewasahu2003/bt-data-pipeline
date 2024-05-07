import time
from dataclasses import dataclass

import pandas as pd
import requests
from ..base import BaseScraper
from bs4 import BeautifulSoup
from ..format import ScrapeFormat

from ..utils import logger
from ...jobs.store import StoreJob, FileFormat


@dataclass
class FunnyShortJokesScraper(BaseScraper):
    """
    Scraper for the 'funnyshortjokes' format.
    """

    format: ScrapeFormat = ScrapeFormat.FUNNYSHORTJOKES
    dp: int = 1
    time: int = None

    def scrape(self) -> dict:
        """
        Scrape the specified URL and return the scraped data as a dictionary.
        """
        if self.format is None:

            logger.info(f"No format specified for {self.dp}")
            return

        logger.info("running scraper for funnyshortjokes")
        start = time.time()

        df_main = pd.DataFrame(columns=["content"])
        CONTENT_CAT = [
            "sports-jokes",
            "animal-jokes",
            "dirty-jokes",
            "disabled-jokes",
            "general-jokes",
            "pick-up-lines",
            "political-jokes",
            "racist-jokes",
            "relationship-jokes",
            "religious-jokes",
            "surreal-jokes",
            "yo-mama-jokes",
        ]

        for cat in CONTENT_CAT:
            current_page = 1
            while True:
                try:
                    logger.info(f"scraping page {current_page} of category {cat}")
                    page_url = (
                        f"https://www.funnyshortjokes.com/c/{cat}/page/{current_page}"
                    )

                    page = requests.get(page_url)
                    print(page.status_code)
                    if page.status_code != 200:
                        break
                    soup = BeautifulSoup(page.content, "html.parser")

                    posts = [
                        post.text.lower().strip()
                        for post in soup.find_all("div", class_="post-text")
                    ]
                    df = pd.DataFrame({"content": posts})
                    df_main = pd.concat([df_main, df], ignore_index=True)
                    del df
                    current_page += 1
                except Exception as e:
                    logger.warn(
                        f"HTTP Error on page {current_page} of category {cat}: "
                    )
                    break

        df_main.drop_duplicates(subset=["content"], inplace=True)
        df_main.reset_index(drop=True, inplace=True)
       # df_main.drop(["Unnamed: 0"], axis=1, inplace=True)
        df_main["content"] = (
            df_main["content"]
            .str.replace(r"[^\x00-\x7F]", "")
            .replace(r"[\r\n]+", " ")
            .str.strip(" ")
        )

        StoreJob.save(file_type=FileFormat.JSONL, df=df_main, filename=self.dp)

        end = time.time()
        self.time = end - start
        logger.info(f"Scraping time for funnyshortjokes is {end-start}s")
