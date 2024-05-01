from scraper.base.main import BaseScraper
from dataclasses import dataclass
from scraper.format import ScrapeFormat
from utils.main import logger
import time
from datasets import load_dataset


@dataclass
class HF5Scraper(BaseScraper):
    """
    Scraper for the 'hf5' format.
    """

    format = ScrapeFormat.HF_5NPCJOKES
    dp = 7

    def scrape(self) -> None:
        """
        Scrape the 'hf5' format and store the data.
        """
        if self.format is None:
            logger.info("No format specified")
            return
        logger.info("Running scraper for HF5 format")
        start = time.time()

        df = load_dataset("pestowithpasta/npc-jokes")
        df_main = df["train"].to_pandas()

        del df

        df_main["content"] = df_main.apply(
            lambda x: str(x["Question"]).lower() + str(x["Answer"]).lower(),
            axis=1,
        )
        df_main.drop_duplicates(subset=["content"], inplace=True)

        df_main.reset_index(drop=True, inplace=True)
        df_main.drop(
            ["Answer", "Question", "ID"],
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

        # uploading datapoint=7
        # TODO: Implement upload_dataset_to_s3 function
        # upload_dataset_to_s3(df_main, "funnyshortjokes")

        del df_main

        end = time.time()
        self.time=end-start
        logger.info(f"Scraping time for dp{self.dp} is {end-start}s")
