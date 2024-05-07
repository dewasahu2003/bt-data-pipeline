from ..base import BaseScraper
from dataclasses import dataclass
from ..format import ScrapeFormat
from ..utils import logger
import time

import pandas as pd
import requests
from ...jobs.store import StoreJob, FileFormat


@dataclass
class LaughFactoryScraper(BaseScraper):
    """
    Scraper for the 'laughfactory' format.
    """

    format: ScrapeFormat = ScrapeFormat.LAUGHFACTORY
    dp: int = 2
    time: int = None

    def scrape(
        self,
    ) -> dict:
        """
        Scrape the specified URL and return the scraped data as a dictionary"""
        if self.format is None:
            logger.info("No format specified")
            return

        logger.info("running scraper for laughfactory")
        start = time.time()

        df_main = pd.DataFrame(columns=["content"])
        CONTENT_CAT = {
            "latest-jokes": "",
            "animal-jokes": 14,
            "blonde-jokes": 24,
            "boycott-these-jokes": 21,
            "clean-jokes": 37,
            "family-jokes": 22,
            "food-jokes": 41,
            "holiday-jokes": 34,
            "insult-jokes": 4,
            "miscellaneous-jokes": 19,
            "office-jokes": 31,
            "political-jokes": 16,
            "pop-culture-jokes": 32,
            "relationship-jokes": 6,
            "religious-jokes": 27,
            "school-jokes": 39,
            "science-jokes": 40,
            "sex-jokes": 20,
            "sports-jokes": 33,
            "technology-jokes": 38,
            "wordplay-jokes": 23,
            "yo-momma-jokes": 8,
        }

        per_page_jokes = 100

        for cat in CONTENT_CAT:
            offset = 0
            while True:
                try:
                    logger.info(f"scraping page {offset} of category {cat}")
                    if cat == "latest-jokes":
                        page_url = f"https://www.laughfactory.com/joke/loadmorejokes?offset={offset}&joke_type=latest&jokes_perpage={per_page_jokes}&kw=&catid="
                    else:
                        page_url = f"https://www.laughfactory.com/joke/loadmorejokes?offset={offset}&joke_type=category&jokes_perpage={per_page_jokes}&kw=&catid={CONTENT_CAT[cat]}"

                    page = requests.get(page_url)
                    jokes = page.json()["jokes"]

                    if jokes is None or len(jokes) == 0:
                        break

                    jockes_stored = []

                    for joke in jokes:
                        joke_text: str = joke["joke_text"]
                        jockes_stored.append(joke_text.lower().strip())

                    df = pd.DataFrame({"content": jockes_stored})
                    df_main = pd.concat([df_main, df], ignore_index=True)
                    del df
                    offset += per_page_jokes

                except Exception as e:
                    logger.error(f"HTTP Error {e} on page {offset} of category {cat}: ")
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
        StoreJob.save(file_type=FileFormat.JSONL, df=df_main, object_name=self.dp)

        end = time.time()
        self.time = end - start
        logger.info(f"Scraping time for laughfactory is {end-start}s")
