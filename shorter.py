import requests
import os
from dotenv import load_dotenv

# Load the values from the .env file
load_dotenv()

SHORTER_API_KEY = os.getenv("SHORTER_API_KEY")
SHORTER_BASE_URL = os.getenv("SHORTER_BASE_URL")


def shorten_link(full_link, link_name=""):
    params = {"key": SHORTER_API_KEY, "short": full_link, "name": link_name}
    response = requests.get(SHORTER_BASE_URL, params=params)
    data = response.json()

    try:
        title = data["url"]["title"]
        short_link = data["url"]["shortLink"]
        return {"title": title, "short_link": short_link, "error": False}

    except KeyError:
        message = "Error"
        status = data["url"]["status"]

        if int(status) == 1:
            message = "the shortened link comes from the domain that shortens the link, i.e. the link has already been shortened"

        elif int(status) == 2:
            message = "the entered link is not a link"

        elif int(status) == 3:
            message = "the preferred link name is already taken"

        return {"message": message, "error": True}
