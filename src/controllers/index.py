import telebot
import re
from env import BOT_TOKEN, SHORT_COMMAND
from utils.index import extract_command_msg, is_valid_url
from utils.instagram import download_instagram_image, download_instagram_video
from utils.shorter import shorten_link

bot = telebot.TeleBot(BOT_TOKEN)

def extract_instagram_post_id(full_url:str) -> str:
    match = re.search(r"(https://www.instagram.com/p/[^/?]+)", full_url)
    if match:
        return match.group(1)
    else:
        return None

def download_instagram_media_controller(message, command: str, media_type: str):
    if len(message.text) < 10:
        error_message = f"🤖: Please insert a valid Instagram post URL. Example: https://www.instagram.com/p/CYZ9o4SrI58"
        return bot.reply_to(message, error_message)

    ig_post_url = extract_command_msg(message.text, command)
    ig_post_url = extract_instagram_post_id(ig_post_url)
    
    if not is_valid_url(ig_post_url) and ig_post_url:
        error_message = f"🤖: Please insert a valid Instagram post URL. Example: https://www.instagram.com/p/CYZ9o4SrI58"
        return bot.reply_to(message, error_message)

    response_message = (
        f"🤖: Downloading your {media_type}, this can take a few seconds..."
    )
    bot.reply_to(message, response_message)
    bot.send_chat_action(message.chat.id, "typing")

    try:
        media_path = None
        media_extension = None

        if media_type == "image":
            media_path = download_instagram_image(ig_post_url)
            media_extension = "jpg"
        else:
            media_path = download_instagram_video(ig_post_url)
            media_extension = "mp4"

        media_file = open(f"{media_path}.{media_extension}", "rb")

        media_caption = f"Your {media_type} 😎"

        if media_type == "image":
            bot.send_photo(message.chat.id, media_file, media_caption)
        else:
            bot.send_video(message.chat.id, media_file, caption=media_caption)

    # TODO: manage JSON Query to graphql/query: HTTP error code 401. error. It is for limit requests
    except Exception as e:
        error_message = (
            f"🤖: An error has occurred while trying to download your {media_type}"
        )
        bot.send_message(message.chat.id, error_message)
        bot.send_message(message.chat.id, "The URL MUST look like this https://www.instagram.com/p/CxY2AL7SjOG/")
        print("fatal error:")


def short_link_controller(message):
    user_msg = str(message.text)

    full_url = extract_command_msg(user_msg, SHORT_COMMAND)

    if not is_valid_url(full_url):
        return bot.reply_to(
            message,
            "🤖: Please insert a valid URL. Example: https://www.joselatines.com/",
            disable_web_page_preview=True,
        )

    bot.reply_to(message, "🤖: Shortening your link...")
    response_link = shorten_link(full_url)

    error = response_link.get("error")
    shorted_link = response_link.get("shorted_link")

    if error:
        return bot.reply_to(
            message,
            f"🤖: An error occurred while shortening the link: {error}",
        )

    bot.send_message(
        message.chat.id,
        f"🤖: Here is your shortened link: {shorted_link}",
        disable_web_page_preview=True,
    )
