from ...jobs.store import StoreJob, FileFormat
from ..base import BaseScraper
from dataclasses import dataclass
from ..format import ScrapeFormat
from ..utils import logger
import time
from datasets import load_dataset


@dataclass
class HF3Scraper(BaseScraper):
    """
    Scraper for the 'hf3' format.
    """

    format: ScrapeFormat = ScrapeFormat.HF_3AMIRKIDJOKES
    dp: int = 5
    time: int = None

    def scrape(
        self,
    ) -> None:
        """
        Scrape the 'hf3' format and store the data.
        """
        if self.format is None:
            logger.info("No format specified")
            return

        logger.info("Running scraper for HF3 format")
        start = time.time()

        df = load_dataset(self.format.value)
        df_main = df["train"].to_pandas()
        df_main.rename(columns={"text": "content"}, inplace=True)
        del df

        df_main.drop_duplicates(subset=["content"], inplace=True)
        df_main.reset_index(drop=True, inplace=True)

        df_main["content"] = (
            df_main["content"]
            .str.replace(r"[^\x00-\x7F]", "")
            .replace(r"[\r\n]+", "")
            .str.strip(" ")
        )
        
        job = StoreJob()
        job.save(file_type=FileFormat.JSONL, df=df_main, object_name=self.dp)
        del job

        end = time.time()
        self.time = end - start
        logger.info(f"Scraping time for funnyshortjokes is {end-start}s")
