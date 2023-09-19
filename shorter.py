import os
import pyshorteners
from dotenv import load_dotenv

# Load the values from the .env file
load_dotenv()

SHORTER_API_KEY = os.getenv("SHORTER_API_KEY")
SHORTER_BASE_URL = os.getenv("SHORTER_BASE_URL")

def shorten_link(full_link:str, link_name=""):
    try:
        shorteners = pyshorteners.Shortener(api_key=SHORTER_API_KEY)
        short_link = shorteners.bitly.short(full_link)
        return {"short_link": short_link, "error": False}
   
    except Exception as e:
        return {"error": str(e)}