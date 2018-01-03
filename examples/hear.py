"""Simple hear with your bot"""

import asyncio

from balebot.filters import TextFilter
from balebot.models.messages import TextMessage
from balebot.updater import Updater

# A token you give from BotFather when you create your bot set below
updater = Updater(token="114d273b48f04cd7c3be657328d2aa5521dae020",
                  loop=asyncio.get_event_loop())
# Define dispatcher
dispatcher = updater.dispatcher


# Both of success and failure functions are optional
def success(result, user_data):
    print("success : ", result)
    print(user_data)


def failure(result, user_data):
    print("failure : ", result)
    print(user_data)


# hear function
@dispatcher.message_handler(filters=TextFilter(keywords=["hello"]))  # filter text the client enter to bot
def hear(bot, update):
    message = TextMessage('Hello')
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)


# Run the bot!
updater.run()
