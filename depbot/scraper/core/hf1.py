from ..base import BaseScraper
from dataclasses import dataclass
from ..format import ScrapeFormat
from ..utils import logger
import time
from datasets import load_dataset


@dataclass
class HF1Scraper(BaseScraper):
    """
    Scraper for the 'hf1' format.
    """

    format:ScrapeFormat = ScrapeFormat.HF_10ENGLISHJOKES
    dp:int=3
    time:int=None

    def scrape(
        self,
    ) -> None:
        """
        Scrape the 'hf1' format and store the data.
        """
        if self.format is None:
            logger.info("No format specified")
            return
        logger.info("Running scraper for HF1 format")
        start = time.time()

        df = load_dataset("Khalida1w/funny_quotes")
        df_main = df["train"].to_pandas()

        df_main.rename(columns={"quote": "content"}, inplace=True)
        del df

        df_main.drop_duplicates(subset=["content"], inplace=True)
        
        df_main.reset_index(drop=True, inplace=True)
        df_main.drop(["author", "tags"], axis=1, inplace=True)
        df_main["content"] = (
            df_main["content"]
            .str.replace(r"[^\x00-\x7F]", "")
            .replace(r"[\r\n]+", " ")
            .str.strip(" ").str.lower()
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
        self.time=end-start
        logger.info(f"Scraping time for funnyshortjokes is {end-start}s")
