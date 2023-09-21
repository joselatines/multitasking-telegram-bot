import telebot
import threading
from env import (
    IMAGES_PATH,
    SHORT_COMMAND,
    SHORT_COMMAND_INFO,
    ABOUT_COMMAND_INFO,
    HELP_COMMAND_INFO,
    IG_IMAGE_COMMAND_INFO,
    ABOUT_COMMAND,
    BOT_TOKEN,
    IG_IMAGE_COMMAND,
    HELP_COMMAND,
    VIDEOS_PATH,
    IG_VIDEO_COMMAND,
    IG_VIDEO_COMMAND_INFO,
)
from utils.index import (
    delete_all_files,
    parse_command,
)
from controllers.index import download_instagram_media_controller, short_link_controller

bot = telebot.TeleBot(BOT_TOKEN)
current_cmd = None


@bot.message_handler(commands=[parse_command(HELP_COMMAND), "ayuda", "help"])
def handle_HELP_COMMAND(message):
    """
    Handles the '/start' command by sending a welcome message.
    """
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(
        message,
        f"🤖: Hi, I'm a multitasking expert! Try {SHORT_COMMAND} to see me in action!",
    )


@bot.message_handler(commands=[parse_command(SHORT_COMMAND), "acortar", "shortener"])
def handle_short_link_command(message):
    """
    Handles the '/short' command by sending a prompt for the link to shorten and setting the current command to 'short'.
    """
    bot.send_chat_action(message.chat.id, "typing")
    msg = bot.send_message(message.chat.id, "Paste URL to short")
    bot.register_next_step_handler(msg, short_link_controller)


@bot.message_handler(commands=[parse_command(ABOUT_COMMAND), "acerca", "aboutme"])
def handle_about_command(message):
    """
    Handles the '/about' command by sending a prompt for the link to shorten and setting the current command to 'short'.
    """
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(
        message,
        "🤖: I am a bot created by the awesome developer José Latines to perform multiple tasks.",
    )


@bot.message_handler(commands=[parse_command(IG_IMAGE_COMMAND)])
def handle_download_ig_image_command(message):
    bot.send_chat_action(message.chat.id, "typing")

    msg = bot.send_message(message.chat.id, "Paste your Instagram post URL")
    bot.register_next_step_handler(
        msg,
        lambda msg: download_instagram_media_controller(msg, IG_IMAGE_COMMAND, "image"),
    )


@bot.message_handler(commands=[parse_command(IG_VIDEO_COMMAND)])
def handle_download_ig_image_command(message):
    bot.send_chat_action(message.chat.id, "typing")

    msg = bot.send_message(message.chat.id, "Paste your Instagram post URL")

    bot.register_next_step_handler(
        msg,
        lambda msg: download_instagram_media_controller(msg, IG_VIDEO_COMMAND, "video"),
    )


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
        bot.send_message(current_chat_id, '🤖: I am a bot, use my commands! "/"')


def start_bot():
    """
    Starts the Telegram bot.
    """
    bot.infinity_polling()


if __name__ == "__main__":
    print("🤖 Bot starts")
    bot.set_my_commands(
        [
            telebot.types.BotCommand(HELP_COMMAND, HELP_COMMAND_INFO),
            telebot.types.BotCommand(SHORT_COMMAND, SHORT_COMMAND_INFO),
            telebot.types.BotCommand(ABOUT_COMMAND, ABOUT_COMMAND_INFO),
            telebot.types.BotCommand(IG_IMAGE_COMMAND, IG_IMAGE_COMMAND_INFO),
            telebot.types.BotCommand(IG_VIDEO_COMMAND, IG_VIDEO_COMMAND_INFO),
        ]
    )
    thread_bot = threading.Thread(name="thread bot", target=start_bot)
    thread_bot.start()
    print("🤖 Bot is running")
    delete_all_files(IMAGES_PATH)
    delete_all_files(VIDEOS_PATH, ".mp4")
