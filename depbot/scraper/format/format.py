from enum import Enum


class ScrapeFormat(Enum):
    """
    The ScrapeFormat Enum class defines the different formats that the scraper can output to.
    """

    FUNNYSHORTJOKES = "funnyshortjokes"
    LAUGHFACTORY = "laughfactory"

    HF_1FUNNYQUOTES = "Khalida1w/funny_quotes"
    HF_2HUMARTRAIN = "lm233/humor_train"
    HF_3AMIRKIDJOKES = "Amirkid/jokes"
    HF_4COUNTRIESJOKES = "Falah/countries_jokes_dataset"
    HF_5NPCJOKES = "pestowithpasta/npc-jokes"
    HF_6DADJOKES = "gnumanth/dad-jokes"
    HF_7OIGJOKES = "orangetin/oig-jokes"
    HF_8MEMEGENJOKE = "Jayeshkumarjangir/memegen_jokes_1217"
    HF_9MYOTHIHAJOKE = "myothiha/jokes"
    HF_10ENGLISHJOKES = "kuldin/english_jokes"
    HF_11FRIDENDS = "yl2342/friends_chandler_bing_sarcasm"
    HF_12FRIENDS = "michellejieli/friends_dataset"
    HF_13FRIENDS = "Teejeigh/raw_friends_series_transcript"
