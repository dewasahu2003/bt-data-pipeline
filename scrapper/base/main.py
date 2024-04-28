from abc import ABC, abstractmethod
from dataclasses import dataclass
from scrapper.format.formats import ScrapeFormat
import json  

@dataclass
class BaseScraper(ABC):
    """
    Abstract base class for all scrapers.
    """
    format: ScrapeFormat = None
    dp: int = None

    @abstractmethod
    def scrape(self,) -> None  :
        """
        Scrape the specified URL and return the scraped data as a dictionary.
        """
        pass
    
    # def store_data(self, data: dict, filename: str):    
    #     """
    #     Store the scraped data to a file.
    #     """
    #     pass
