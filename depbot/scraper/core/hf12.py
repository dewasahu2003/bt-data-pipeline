from base import BaseScraper
from dataclasses import dataclass
from format import ScrapeFormat
from utils import logger
import time
from datasets import load_dataset


@dataclass
class HF12Scraper(BaseScraper):
    """
    Scraper for the 'hf12' format.
    """

    format:ScrapeFormat = ScrapeFormat.HF_12FRIENDS
    dp:int = 14
    time:int = None

    def scrape(self) -> None:
        """
        Scrape the 'hf12' format
        """

        if self.format is None:
            logger.info("No format specified")
            return

        logger.info("Running scraper for HF12 format")
        start = time.time()

        df = load_dataset("michellejieli/friends_dataset")

        df_main = df["train"].to_pandas()
        del df

        df_main.rename(columns={"text": "content"}, inplace=True)
        df_main.drop_duplicates(subset=["content"], inplace=True)

        df_main.reset_index(drop=True, inplace=True)
        df_main.drop(
            ["label"],
            axis=1,
            inplace=True,
        )
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
        self.time = end - start
        logger.info(f"Scraping time for dp{self.dp} is {end-start}s")
