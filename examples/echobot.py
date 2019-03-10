#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Bale messages.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from balebot.filters import DefaultFilter
from balebot.handlers import CommandHandler, MessageHandler
from balebot.updater import Updater
from balebot.utils.logger import Logger

# Enable logging
logger = Logger.get_logger()


# Define a few command handlers. These usually take the two arguments bot and
def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.reply(update, 'Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    bot.reply(update, 'Help!')


def echo(bot, update):
    """Echo the user message."""
    message = update.get_effective_message()
    bot.reply(update, message)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.error('Update {} caused error {}'.format(update, error), extra={"tag": "err"})


def main():
    """Start the bot."""
    # Bale Bot Authorization Token
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Bale
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Bale
    dp.add_handler(MessageHandler(DefaultFilter(), echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.run()


if __name__ == '__main__':
    main()
