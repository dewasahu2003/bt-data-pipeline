from ..base import BaseScraper
from dataclasses import dataclass
from ..format import ScrapeFormat
from ..utils import logger
import time
from datasets import load_dataset
from ...jobs.store import StoreJob,FileFormat
import pandas as pd


@dataclass
class HF9Scraper(BaseScraper):
    """
    Scraper for the 'hf9' format.
    """

    format:ScrapeFormat = ScrapeFormat.HF_9MYOTHIHAJOKE
    dp:int = 11
    time:int = None

    def scrape(self) -> None:
        """
        Scrape the 'hf9' format and
        """
        if self.format is None:
            logger.info("No format specified")
            return

        logger.info("Running scraper for HF9 format")
        start = time.time()

        df = load_dataset(self.format.value)

        df_main = pd.concat(
            [
                df["train"].to_pandas(),
                df["validation"].to_pandas(),
                df["test"].to_pandas(),
            ],
            axis=0,
        )
        del df
        df_main["text"] = df_main["text"].astype(str)

        df_main.rename(columns={"text": "content"}, inplace=True)
        # df_main["content"] = df_main.apply(
        #     lambda x: str(x["prompt"]) + str(x["completion"]),
        #     axis=1,
        # )
        df_main.drop_duplicates(subset=["content"], inplace=True)

        df_main.reset_index(drop=True, inplace=True)
        df_main.drop(
            ["Unnamed: 0"],
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

        job = StoreJob()
        job.save(file_type=FileFormat.JSONL, df=df_main, object_name=self.dp)
        del job

        end = time.time()
        self.time = end - start
        logger.info(f"Scraping time for dp{self.dp} is {end-start}s")
