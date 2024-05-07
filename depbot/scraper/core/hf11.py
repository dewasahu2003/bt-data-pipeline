from ..base import BaseScraper
from dataclasses import dataclass
from ..format import ScrapeFormat
from ..utils import logger
import time
from datasets import load_dataset
from ...jobs.store import StoreJob, FileFormat


@dataclass
class HF11Scraper(BaseScraper):
    """
    Scraper for the 'hf11' format.
    """

    format: ScrapeFormat = ScrapeFormat.HF_11FRIDENDS
    dp: int = 13
    time: int = None

    def scrape(self) -> None:
        """
        Scrape the 'hf11' format and
        """
        if self.format is None:
            logger.info("No format specified")
            return

        logger.info("Running scraper for HF11 format")
        start = time.time()

        df = load_dataset("yl2342/friends_chandler_bing_lines_sarcasm")

        df_main = df["train"].to_pandas()
        del df

        df_main["content"] = df_main.apply(
            lambda x: f"Chandler_quote: {x['Chandler_quote']} Context: {x['Context']} Reason: {x['Reason']} Unlike_chandler_sarcastic: {x['Unlike_chandler_sarcastic']} Unlike_chandler_sincere: {x['Unlike_chandler_sincere']}",
            axis=1,
        )

        df_main.drop_duplicates(subset=["content"], inplace=True)

        df_main.reset_index(drop=True, inplace=True)
        df_main.drop(
            [
                "Chandler_quote",
                "Context",
                "Sarcasm",
                "Reason",
                "Unlike_chandler_sarcastic",
                "Unlike_chandler_sincere",
                "episode",
            ],
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
