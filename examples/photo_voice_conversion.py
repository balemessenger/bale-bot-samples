"""Text simple conversion with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.updater import Updater


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
    message = TextMessage("Hi , nice to meet you :)\nplease send me your photo.")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(PhotoFilter(), ask_photo),
                                                                MessageHandler(DefaultFilter(), skip_photo)])


def ask_photo(bot, update):
    message = TextMessage("Thanks \nplease send a voice message")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(VoiceFilter(), finish_conversion))


def skip_photo(bot, update):
    message = TextMessage("So, you don't want to send me your photo !\nplease just give a voice message :(")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(VoiceFilter(), finish_conversion))


def finish_conversion(bot, update):
    message = TextMessage("Thanks \ngoodbye ;)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
