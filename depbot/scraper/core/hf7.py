from ..base import BaseScraper
from dataclasses import dataclass
from ..format import ScrapeFormat
from ..utils import logger
import time
from datasets import load_dataset
from ...jobs.store import StoreJob, FileFormat

@dataclass
class HF7Scraper(BaseScraper):
    """
    Scraper for the 'hf7' format.
    """

    format:ScrapeFormat = ScrapeFormat.HF_7OIGJOKES
    dp:int = 9
    time:int = None

    def scrape(self) -> None:
        """
        Scrape the 'hf7' format and store the data.
        """
        if self.format is None:
            logger.info("No format specified")
            return
        logger.info("Running scraper for HF7 format")
        start = time.time()

        df = load_dataset(self.format.value)
        df_main = df["train"].to_pandas()
        del df

        df_main.rename(columns={"text": "content"}, inplace=True)
        df_main.drop(
            ["metadata"],
            axis=1,
            inplace=True,
        )
        df_main.drop_duplicates(subset=["content"], inplace=True)

        df_main.reset_index(drop=True, inplace=True)

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
        self.time=end-start
        logger.info(f"Scraping time for dp{self.dp} is {end-start}s")
