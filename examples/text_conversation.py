#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Text simple conversation with bot."""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.updater import Updater
from balebot.utils.logger import Logger

# Bale Bot Authorization Token
updater = Updater(token="TOKEN",
                  loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher

# Enable logging
logger = Logger.get_logger()


def success_send_message(response, user_data):
    kwargs = user_data['kwargs']
    update = kwargs["update"]
    user_peer = update.get_effective_user()
    logger.info("Your message has been sent successfully.", extra={"user_id": user_peer.peer_id, "tag": "info"})


def failure_send_message(response, user_data):
    kwargs = user_data['kwargs']
    update = kwargs["update"]
    user_peer = update.get_effective_user()
    logger.error("Sending message has been failed", extra={"user_id": user_peer.peer_id, "tag": "error"})


@dispatcher.command_handler(["/start"])
def conversation_starter(bot, update):
    message = TextMessage("*Hi , nice to meet you*\nplease tell me your name.")
    # Get client user object by a function called (get_effective_user)
    user_peer = update.get_effective_user()
    # Set any user data in kwargs mode
    kwargs = {"message": message, "update": update}
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    # You can put more than one Filters for your handler
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), ask_name),
                                                                MessageHandler(DefaultFilter(), skip_name)])


def ask_name(bot, update):
    message = TextMessage("*Thanks!*\nplease tell me your age")
    user_peer = update.get_effective_user()
    # Get client message object by a function called (get_effective_message)
    name_obj = update.get_effective_message()
    # Get text form a message obj
    name_text = name_obj.text
    # Set a conversation data in RAM (Not durable)
    dispatcher.set_conversation_data(update=update, key="name", value=name_text)
    kwargs = {"message": message, "update": update}
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update,
                                                       # Set Regex pattern for TextFilter
                                                       MessageHandler(TextFilter(pattern="^[0-9]+$"),
                                                                      finish_conversion))


def skip_name(bot, update):
    message = TextMessage("*So, you don't want to tell your name!*\nplease just tell me your age")
    user_peer = update.get_effective_user()
    kwargs = {'update': update}
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    no_name = "no name"
    dispatcher.set_conversation_data(update=update, key="name", value=no_name)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), finish_conversion))


def finish_conversion(bot, update):
    message = TextMessage("*Thanks!*\ngoodbye ;)")
    user_peer = update.get_effective_user()
    kwargs = {'update': update}
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    name = dispatcher.get_conversation_data(update, key="name")
    age = update.get_effective_message().text
    output = TextMessage("*Name:* " + name + "\n" + "*Age:* " + age)
    bot.send_message(output, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    dispatcher.finish_conversation(update)


if __name__ == '__main__':
    updater.run()
