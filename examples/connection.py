# -*- coding: utf-8 -*-
"""Its a simple example of connection between your bot and Bale server.
At first you need to connect to server with your bot's token that you've given before.
Second you import Updater and create your object updater and dispatcher from it. Next you need some
functions, you defined before and two optional functions (success and failure) in order to log success
and failure locally.
At end you need updater.run() to run your bot and enjoy!
"""
import asyncio

from balebot.updater import Updater

# A token you give from BotFather when you create your bot set below
updater = Updater(token="114d273b48f04cd7c3be657328d2aa5521dae020",
                  loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher


def success(result, user_data):
    print("success : ", result)
    print(user_data)


def failure(result, user_data):
    print("failure : ", result)
    print(user_data)


@dispatcher.error_handler()
def error_handler(bot, update, error):
    if update:
        print(update)
    print(error, "  :  handled by error_handler")


@dispatcher.default_handler()
def default_handler_func(bot, update):
    bot.respond(update, "default handler is replying.".format(), success_callback=success,
                failure_callback=failure)


updater.run()
