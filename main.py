import os
from dotenv import load_dotenv
import telebot
import threading
from shorter import shorten_link

# Load the values from the .env file
load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

START_COMMAND = "/start"
SHORT_COMMAND = "/short"
ABOUT_COMMAND = "/about"

current_cmd = None



@bot.message_handler(commands=[START_COMMAND, 'start',"ayuda", "help"])
def handle_start_command(message):
    """
    Handles the '/start' command by sending a welcome message.
    """
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, f"🤖: Hi I'am a shortener expert, try {SHORT_COMMAND} to see me working!")


@bot.message_handler(commands=[SHORT_COMMAND, "short", "acortar", "shortener"])
def handle_short_link_command(message):
    """
    Handles the '/short' command by sending a prompt for the link to shorten and setting the current command to 'short'.
    """
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(
        message, "🤖: Please insert your link with the short name: www.example.com"
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
        message, "🤖: I am a bot created by the awesome developer José Latines"
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
            current_chat_id, "🤖: I don't know that command or is not available"
        )

    elif current_cmd == "short":
        res_shorted_link = shorten_link(message.text)
        if res_shorted_link["error"]:
          res_msg = f'🤖❌: {res_shorted_link["message"].capitalize()}'
          bot.send_message(current_chat_id, res_msg)

        else:
            bot.send_message(
                current_chat_id,
                f"🤖✅: Here is your link: {res_shorted_link['short_link']}",
            )

            current_cmd = None

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
            telebot.types.BotCommand(START_COMMAND, "Say hello to the bot!"),
            telebot.types.BotCommand(SHORT_COMMAND, "Enter a link to short it"),
            telebot.types.BotCommand(ABOUT_COMMAND, "More details about me"),
        ]
    )
    thread_bot = threading.Thread(name="thread bot", target=start_bot)
    thread_bot.start()
    print("🤖 Bot running")
