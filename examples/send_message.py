"""Simple Bot to reply,text message and send and receive message for Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import asyncio

from balebot.filters import *
from balebot.models.messages import *
from balebot.updater import Updater
from balebot.utils.logger import Logger
from Config import Config

# A token you give from BotFather when you create your bot set below
updater = Updater(token="114d273b48f04cd7c3be657328d2aa5521dae020",
                  loop=asyncio.get_event_loop())

bot = updater.bot  # define bot
dispatcher = updater.dispatcher
Lg = Logger.get_logger()  # get a logger from bot SDK
Lg.use_graylog = Config.use_graylog  # if you set it True, it means use graylog
Lg.graylog_host = Config.graylog_host
Lg.graylog_port = Config.graylog_port
Lg.log_level = Config.log_level  # set log level
Lg.log_facility_name = Config.log_facility_name


def success(result, user_data):
    print("success : ", result)
    print(user_data)


def failure(result, user_data):
    print("failure : ", result)
    print(user_data)


@dispatcher.command_handler("reply_it")
def replay_message(bot, update):
    bot.reply(update, "replied message", success_callback=success, failure_callback=failure)
    Lg.info("message is replied successfully")


@dispatcher.message_handler(filters=[TextFilter(keywords=["iran", "python", "سلام"], pattern="^hello(.)+"),
                                     TemplateResponseFilter(keywords=["say_hello"])])
def text_received(bot, update):
    message = TextMessage('filtered text received')
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)


@dispatcher.message_handler(ContactFilter())
def contact_received(bot, update):
    message = update.get_effective_message()
    user_peer = update.get_effective_user()
    bot.reply(update, "it is a contact", success_callback=success, failure_callback=failure)
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)


@dispatcher.message_handler(LocationFilter())
def location_received(bot, update):
    bot.reply(update, "it is a location", success_callback=success, failure_callback=failure)


@dispatcher.message_handler(DocumentFilter())
def some_document_file_received(bot, update):
    message = update.get_effective_message()
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    print(update.body.message.file_id)
    bot.get_file_download_url(message.file_id, user_peer.peer_id, "file", success_callback=success,
                              failure_callback=failure)


@dispatcher.message_handler([VoiceFilter(), VideoFilter()])
def some_vv_file_received(bot, update):
    message = update.get_effective_message()
    bot.reply(update, message, success_callback=success, failure_callback=failure)


@dispatcher.command_handler("/start")
def start_command(bot, update):
    message = update.get_effective_message()
    bot.respond(update, message, success_callback=success, failure_callback=failure)


@dispatcher.command_handler(["/skip", "/help"])
def skip_or_help_command_received(bot, update):
    bot.reply(update, "do you need help?\nor you want to skip?", success_callback=success, failure_callback=failure)


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
