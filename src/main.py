import telebot
import threading
from env import (
    SHORT_COMMAND,
    SHORT_COMMAND_INFO,
    ABOUT_COMMAND_INFO,
    START_COMMAND_INFO,
    IG_IMAGE_COMMAND_INFO,
    ABOUT_COMMAND,
    BOT_TOKEN,
    IG_IMAGE_COMMAND,
    START_COMMAND,
)
from utils.shorter import shorten_link
from utils.instagram import download_instagram_image
from utils.index import extract_command_msg, is_valid_url, delete_file,delete_all_files

bot = telebot.TeleBot(BOT_TOKEN)
current_cmd = None

@bot.message_handler(commands=[START_COMMAND, "start", "ayuda", "help"])
def handle_start_command(message):
    """
    Handles the '/start' command by sending a welcome message.
    """
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(
        message,
        f"🤖: Hi, I'm a multitasking expert! Try {SHORT_COMMAND} to see me in action!",
    )


@bot.message_handler(commands=[SHORT_COMMAND, "short", "acortar", "shortener"])
def handle_short_link_command(message):
    """
    Handles the '/short' command by sending a prompt for the link to shorten and setting the current command to 'short'.
    """
    bot.send_chat_action(message.chat.id, "typing")

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

    global current_cmd
    current_cmd = "short"


@bot.message_handler(commands=[ABOUT_COMMAND, "about", "acerca", "aboutme"])
def handle_about_command(message):
    """
    Handles the '/about' command by sending a prompt for the link to shorten and setting the current command to 'short'.
    """
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(
        message,
        "🤖: I am a bot created by the awesome developer José Latines to perform multiple tasks.",
    )


@bot.message_handler(commands=[IG_IMAGE_COMMAND, "igimage"])
def handle_download_ig_image_command(message):
    bot.send_chat_action(message.chat.id, "typing")

    if len(message.text) < 10:
        return bot.reply_to(
            message,
            f"🤖: Please insert a valid Instagram post URL. Example: {IG_IMAGE_COMMAND} https://www.instagram.com/p/CYZ9o4SrI58",
        )

    user_msg = extract_command_msg(message.text, IG_IMAGE_COMMAND)

    if not is_valid_url(user_msg):
        return bot.reply_to(
            message,
            f"🤖: Please insert a valid Instagram post URL. Example: {IG_IMAGE_COMMAND} https://www.instagram.com/p/CYZ9o4SrI58",
        )

    bot.reply_to(
        message,
        "🤖: Downloading your image, this can take a few seconds...",
    )
    bot.send_chat_action(message.chat.id, "typing")

    try:
        img_path = download_instagram_image(user_msg)

        photo = open(f"{img_path}.jpg", "rb")

        bot.send_photo(message.chat.id, photo, "Your image 😎")

        # delete saved image after show to user
       

    except Exception as e:
          bot.send_message(message.chat.id, "🤖: An error has occurred while trying to download your image")
          print("fatal error:", e)
          


@bot.message_handler(content_types=["text"])
def handle_text_message(message):
    """
    Handles incoming text messages by checking if they are a command or a response to a current command.
    """
    global current_cmd
    bot.send_chat_action(message.chat.id, "typing")
    current_chat_id = message.chat.id
    user_msg = str(message.text)

    if user_msg.startswith("/"):
        bot.send_message(
            current_chat_id, "🤖: I don't recognize that command or it's not available"
        )
    else:
        bot.send_message(current_chat_id, "🤖: I am a bot, use my commands!")


def start_bot():
    """
    Starts the Telegram bot.
    """
    bot.infinity_polling()


if __name__ == "__main__":
    print("🤖 Bot starts")
    bot.set_my_commands(
        [
            telebot.types.BotCommand(START_COMMAND, START_COMMAND_INFO),
            telebot.types.BotCommand(SHORT_COMMAND, SHORT_COMMAND_INFO),
            telebot.types.BotCommand(ABOUT_COMMAND, ABOUT_COMMAND_INFO),
            telebot.types.BotCommand(IG_IMAGE_COMMAND, IG_IMAGE_COMMAND_INFO),
        ]
    )
    thread_bot = threading.Thread(name="thread bot", target=start_bot)
    thread_bot.start()
    print("🤖 Bot is running")
    delete_all_files()
