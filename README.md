# Telegram Link Shortener Bot
This is a Telegram bot that can be used to shorten URLs.

## How to Use
1. Start the bot by sending a message with the command "/start".
2. To shorten a link, send a message with the command "/short" or one of its aliases: "acortar", "shortener".
3. The bot will prompt you to insert the URL to shorten.
4. After entering the URL, the bot will return the shortened link.

## Commands
The following commands are available for the bot:

- /start, ayuda, help: Displays a welcome message.
- /short, acortar, shortener: Prompts for the URL to shorten.
- /about, acerca, aboutme: Displays information about the bot.

## Installation
1. Clone this repository.
2. Install the required packages by running pip install -r requirements.txt.
3. Create a .env file and add your Telegram bot token as the value for the TELEGRAM_TOKEN key. Example: TELEGRAM_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuv.
4. Run the bot by executing python main.py.

## Dependencies
os
dotenv
telebot
threading
shorter (a custom module created by the developer)