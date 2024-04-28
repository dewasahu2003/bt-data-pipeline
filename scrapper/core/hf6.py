from base.main import BaseScraper
from dataclasses import dataclass
from scrapper.format.formats import ScrapeFormat
from utils.logger import logger
import time
from datasets import load_dataset
import pandas as pd

@dataclass
class HF6Scraper(BaseScraper):
    """
    Scraper for the 'hf6' format.
    """

    format = ScrapeFormat.HF_6DADJOKES
    dp = 8

    def scrape(self) -> None:
        """
        Scrape the 'hf6' format and store the data.
        """
        if self.format is None:
            logger.info("No format specified")
            return
        logger.info("Running scraper for HF6 format") 
        start = time.time()

        df = load_dataset("gnumanth/dad-jokes")
        df_main:pd.DataFrame = pd.concat(
            [df["train"].to_pandas(), df["test"].to_pandas()], ignore_index=True
        )
        df_main.rename(columns={"joke": "content"}, inplace=True)
        df_main.drop(
            ["id", "name"],
            axis=1,
            inplace=True,
        )
        del df

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
        # uploading datapoint=8
        # TODO: Implement upload_dataset_to_s3 function
        # upload_dataset_to_s3(df_main, "funnyshortjokes")

        del df_main

        end = time.time()
        logger.info(f"Scraping time for dp{self.dp} is {end-start}s")
