from base.main import BaseScraper
from dataclasses import dataclass
from scrapper.format.formats import ScrapeFormat
from utils.logger import logger
import time
from datasets import load_dataset


@dataclass
class HF13Scraper(BaseScraper):
    """
    Scraper for the 'hf13' format.
    """

    format = ScrapeFormat.HF_13FRIENDS
    dp = 15

    def scrape(self) -> None:
        """
        Scrape the 'hf13' format and store the data.
        """
        if self.format is None:
            logger.info("No format specified")
            return
        logger.info("Running scraper for HF13 format")
        start = time.time()

        df = load_dataset("Teejeigh/raw_friends_series_transcript")
        df_main = df["train"].to_pandas()
        del df

        df_main.rename(columns={"text": "content"}, inplace=True)
        df_main.drop_duplicates(subset=["content"], inplace=True)

        df_main.reset_index(drop=True, inplace=True)
        df_main["content"] = (
            df_main["content"]
            .str.replace(r"[^\x00-\x7F]", "")
            .replace(r"[\r\n]+", "")
            .str.strip("")
            .str.lower()
        )
        df_main = df_main.to_json(
            orient="records",
            lines=True,
            force_ascii=False,
        )
        # uploading datapoint=9
        # TODO: Implement upload_dataset_to_s3 function
        # upload_dataset_to_s3(df_main, "funnyshortjokes")

        del df_main

        end = time.time()
        logger.info(f"Scraping time for dp{self.dp} is {end-start}s")
