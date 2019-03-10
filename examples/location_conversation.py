#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Location message conversation with bot."""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.models.messages.location_message import LocationMessage
from balebot.updater import Updater
from balebot.utils.logger import Logger

# Bale Bot Authorization Token
updater = Updater(token="TOKEN",
                  loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher

# Enable logging
logger = Logger.get_logger()


def success_send_message(response, user_data):
    logger.info("Your message has been sent successfully.", extra={"tag": "info"})


def failure_send_message(response, user_data):
    logger.error("Sending message has been failed", extra={"tag": "error"})


@dispatcher.message_handler(filters=LocationFilter())
def conversation_starter(bot, update):
    user_peer = update.get_effective_user()
    general_message = TextMessage("Hi ,Are you hungry?")
    btn_list = [TemplateMessageButton(text="yes", value="yes", action=0),
                TemplateMessageButton(text="no", value="no", action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message)
    dispatcher.register_conversation_next_step_handler(
        update, [MessageHandler(TemplateResponseFilter(keywords=["yes"]), find_location),
                 MessageHandler(TemplateResponseFilter(keywords=["no"]), no_thanks)])


def no_thanks(bot, update):
    bot.reply(update, "It's Ok.", success_callback=success_send_message, failure_callback=failure_send_message)
    dispatcher.finish_conversation(update)


def find_location(bot, update):
    user_peer = update.get_effective_user()
    bot.reply(update, "Here is a good restaurant sir.", success_callback=success_send_message,
              failure_callback=failure_send_message)
    # Make a location from LocationMessage and send it.
    location_message = LocationMessage(longitude="51.41714821748457", latitude="35.73122955392002")
    bot.send_message(location_message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message)
    dispatcher.finish_conversation(update)


if __name__ == '__main__':
    updater.run()
