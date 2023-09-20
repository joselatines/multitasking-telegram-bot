import os
from dotenv import load_dotenv

# Load the values from the .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

START_COMMAND = "/start"
START_COMMAND_INFO = "Say hello to the bot!"
SHORT_COMMAND = "/short"
SHORT_COMMAND_INFO = str(
    f"Enter a link to short it. Example: {SHORT_COMMAND} https://www.joselatines.com/"
)

ABOUT_COMMAND = "/about"
ABOUT_COMMAND_INFO = "More details about me"
IG_IMAGE_COMMAND = "/igimage"
IG_IMAGE_COMMAND_INFO = str(
    f"Download instagram photo by url. {IG_IMAGE_COMMAND} https://www.instagram.com/p/CoXXh4FOE_Z/"
)
