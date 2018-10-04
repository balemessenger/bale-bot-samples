"""Simple Bot to Reply to Bale messages."""

import asyncio

from balebot.filters import DefaultFilter
from balebot.models.messages import TextMessage
from balebot.updater import Updater

# Bale Bot Authorization Token
updater = Updater(token="PUT YOUR TOKEN HERE",
                  loop=asyncio.get_event_loop())
# Define dispatcher
dispatcher = updater.dispatcher


# Both of success and failure functions are optional
def success(response, user_data):
    print("success : ", response)
    print(user_data)


def failure(response, user_data):
    print("failure : ", response)
    print(user_data)


@dispatcher.message_handler(filters=DefaultFilter())
def echo(bot, update):
    message = TextMessage('*Hello*')
    # Send a message to client
    bot.reply(update, message, success_callback=success, failure_callback=failure)


# Run the bot!
updater.run()
