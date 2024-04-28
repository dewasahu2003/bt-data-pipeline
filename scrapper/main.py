import requests
from bs4 import BeautifulSoup
from src.format.format import ScrapeFormat
from src.utils.logger import logger
from dataclasses import dataclass
import time
from src.store.s3_utils import upload_dataset_to_s3


# for exp
import pandas as pd


@dataclass
class Scraper:
    """
    Scraper class to scrape the specified format.
    ### if scrapping more than 5 websites in future with complex logic,then make seprate class for all other formats.
    """

    format: ScrapeFormat = None

    def run(self):
        """
        Run the scraper for the specified format.
        """

        if self.format is None:
            print("No format specified")
            return

        if self.format == ScrapeFormat.FUNNYSHORTJOKES:
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
                        page_url = f"https://www.funnyshortjokes.com/c/{cat}/page/{current_page}"

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
                        current_page += 1
                    except Exception as e:
                        logger.warn(
                            f"HTTP Error on page {current_page} of category {cat}: "
                        )
                        break

            print(df_main.describe())
            df_main.drop_duplicates(subset=["content"], inplace=True)
            df_main.reset_index(drop=True, inplace=True)
            # df.to_csv("funnyshortjokes.csv")

            # upload_dataset_to_s3(df_main, "funnyshortjokes")

            # df_main.to_feather("funnyshortjokes.feather")
            end = time.time()
            logger.info(f"Scraping time for funnyshortjokes is {end-start}s")

            df_main.to_csv("funnyshortjokes.csv")

        elif self.format == ScrapeFormat.LAUGHFACTORY:
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
                        offset += per_page_jokes

                    except Exception as e:
                        logger.error(
                            f"HTTP Error {e} on page {offset} of category {cat}: "
                        )
                        break

            print(df_main.describe())

            df_main.drop_duplicates(subset=["content"], inplace=True)
            df_main.reset_index(drop=True, inplace=True)
            # df.to_csv("laughfactory.csv")

            #upload_dataset_to_s3(df_main, "laughfactory")
            # df_main.to_feather("laughfactory.feather")
            df_main.to_csv("laughfactory.csv")

            end = time.time()
            logger.info(f"Scraping time for laughfactory is {end-start}s")
