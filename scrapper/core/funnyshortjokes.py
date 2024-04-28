from bs4 import BeautifulSoup
from base.main import BaseScraper
from dataclasses import dataclass
from scrapper.format.formats import ScrapeFormat
from utils.logger import logger
import time
import pandas as pd
import requests


@dataclass
class FunnyShortJokesScraper(BaseScraper):
    """
    Scraper for the 'funnyshortjokes' format.
    """

    format = ScrapeFormat.FUNNYSHORTJOKES
    dp = 1

    def scrape(self, url: str) -> dict:
        """
        Scrape the specified URL and return the scraped data as a dictionary.
        """
        if self.format is None:
            logger.info("No format specified")
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
        df_main.drop(["Unnamed: 0"], axis=1, inplace=True)
        df_main["content"] = (
            df_main["content"]
            .str.replace(r"[^\x00-\x7F]", "")
            .replace(r"[\r\n]+", " ")
            .str.strip(" ")
        )
        df_main = df_main.to_json(
            orient="records",
            lines=True,
            force_ascii=False,
        )

        # uploading datapoint=1
        # TODO: Implement upload_dataset_to_s3 function
        # upload_dataset_to_s3(df_main, "funnyshortjokes")

        del df_main

        end = time.time()
        logger.info(f"Scraping time for funnyshortjokes is {end-start}s")
