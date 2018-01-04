"""Text simple conversion with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.updater import Updater
from balebot.utils.logger import Logger
from Config import Config

# A token you give from BotFather when you create your bot set below
updater = Updater(token="114d273b48f04cd7c3be657328d2aa5521dae020",
                  loop=asyncio.get_event_loop())
bot = updater.bot
dispatcher = updater.dispatcher


def success(result, user_data):
    print("success : ", result)
    print(user_data)


def failure(result, user_data):
    print("failure : ", result)
    print(user_data)


@dispatcher.command_handler(["talk"])
def conversation_starter(bot, update):
    message = TextMessage("Hi , nice to meet you :)\nplease tell me your name.")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), ask_name),
                                                                MessageHandler(DefaultFilter(), skip_name)])


def ask_name(bot, update):
    message = TextMessage("Thanks \nplease tell me your age")
    user_peer = update.get_effective_user()
    name = update.body.message.text
    dispatcher.set_conversation_data(update=update, key="name", value=name)  # set a key and value in RAM (Not durable)
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), finish_conversion))


def skip_name(bot, update):
    message = TextMessage("So, you don't want to tell your name !\nplease just tell me your age")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), finish_conversion))


def finish_conversion(bot, update):
    message = TextMessage("Thanks \ngoodbye ;)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    name = dispatcher.get_conversation_data(update, key="name")
    age = update.body.message.text
    output = TextMessage(name + age)
    bot.send_message(output, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
