import os
import pyshorteners
from dotenv import load_dotenv

# Load the values from the .env file
load_dotenv()

SHORTER_API_KEY = os.getenv("SHORTER_API_KEY")
SHORTER_BASE_URL = os.getenv("SHORTER_BASE_URL")


def shorten_link(full_link: str, link_name: str = "") -> dict:
    print(full_link, "shorten links")
    try:
        shorteners = pyshorteners.Shortener(api_key=SHORTER_API_KEY)
        shorted_link = shorteners.bitly.short(full_link)
        return {"shorted_link": shorted_link, "error": False}

    except Exception as e:
        print(e)
        return {"shorted_link": None, "error": str(e)}
