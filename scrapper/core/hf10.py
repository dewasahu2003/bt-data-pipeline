from base.main import BaseScraper
from dataclasses import dataclass
from scrapper.format.formats import ScrapeFormat
from utils.logger import logger
import time
from datasets import load_dataset


@dataclass
class HF10Scraper(BaseScraper):
    """
    Scraper for the 'hf10' format.
    """

    format = ScrapeFormat.HF_10ENGLISHJOKES
    dp = 12

    def scrape(self) -> None:
        """
        Scrape the 'hf10' format
        """
        if self.format is None:
            logger.info("No format specified")
            return

        logger.info("Running scraper for HF10 format")
        start = time.time()

        df = load_dataset("kuldin/english_jokes")
        df_main = df["train"].to_pandas()

        del df

        # df_main.rename(columns={"text": "content"}, inplace=True)
        df_main["content"] = df_main.apply(
            lambda x: str(x["body"]) + str(x["title"]),
            axis=1,
        )
        df_main.drop_duplicates(subset=["content"], inplace=True)

        df_main.reset_index(drop=True, inplace=True)
        df_main.drop(
            ["id", "score", "title", "body"],
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
        logger.info(f"Scraping time for dp{self.dp} is {end-start}s")
