#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple Bot to reply messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import logging
from time import sleep

import telegram
from telegram.error import NetworkError, Unauthorized

update_id = None


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(token='send:42520920:7819b391bb76f56f9f3c3859b992f6e00c96dd75',
                       base_url="https://tapi.bale.ai/")

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        bot.delete_webhook()
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    while True:
        try:
            echo(bot)
            sleep(2)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            update.message.reply_text(update.message.text)


if __name__ == '__main__':
    main()
