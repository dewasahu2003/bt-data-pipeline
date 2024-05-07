from ..base import BaseScraper
from dataclasses import dataclass
from ..format import ScrapeFormat
from ..utils import logger
import time
from datasets import load_dataset
from ...jobs.store import StoreJob, FileFormat


@dataclass
class HF10Scraper(BaseScraper):
    """
    Scraper for the 'hf10' format.
    """

    format:ScrapeFormat = ScrapeFormat.HF_10ENGLISHJOKES
    dp:int = 12
    time:int = None

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
        StoreJob.save(file_type=FileFormat.JSONL, df=df_main, filename=self.dp)

        end = time.time()
        self.time = end - start
        logger.info(f"Scraping time for dp{self.dp} is {end-start}s")
