# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from uuid import uuid4

import re

from telegram import InlineQueryResultArticle, ParseMode, \
InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import logging
from pyshorteners import Shortener

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
    title="with Google",
    input_message_content=InputTextMessageContent(
    shorten("Google", query),
    parse_mode=ParseMode.HTML)))

    results.append(InlineQueryResultArticle(id=uuid4(),
    title="with Bit.ly",
    input_message_content=InputTextMessageContent(
    shorten("Bitly", query),
    parse_mode=ParseMode.HTML)))

    update.inline_query.answer(results)

def shorten(website, link):
    print(link)
    if website == "Bitly":
        bitly = "a3711a7b536d591236a934b81ad6316fd7095bb8"
        shortener = Shortener('Bitly', bitly_token=bitly)
        try:
            result = shortener.short(link)
            return result
        except:
            return "enter a valid url"
    if website == "Google":
        api_key = "AIzaSyAENcBzlF5fK8lgopX38n8o9u8gLBEmNFc"
        shortener = Shortener('Google', api_key=api_key)
        try:
            result = shortener.short(link)
            # print("result")
            return result
        except:
            return "url invalid"
    return "enter a valid url"

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("437994771:AAE8PBAfnbzUc7rwii-qR3EMO31ZQHgxHtI")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()