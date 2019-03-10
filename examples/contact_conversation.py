#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contact message conversation with bot."""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.models.messages.contact_message import ContactMessage
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


@dispatcher.message_handler(filters=ContactFilter())  # filter text the client enter to bot
def conversation_starter(bot, update):
    user_peer = update.get_effective_user()
    general_message = TextMessage("Hi ,I receive your contact, Can I send you a contact too?")
    btn_list = [TemplateMessageButton(text="yes", value="yes", action=0),
                TemplateMessageButton(text="no", value="no", action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message)
    dispatcher.register_conversation_next_step_handler(
        update, [MessageHandler(TemplateResponseFilter(keywords=["yes"]), send_contact),
                 MessageHandler(TemplateResponseFilter(keywords=["no"]), no_thanks)])


def no_thanks(bot, update):
    bot.reply(update, "It's Ok.", success_callback=success_send_message, failure_callback=failure_send_message)
    dispatcher.finish_conversation(update)


def send_contact(bot, update):
    user_peer = update.get_effective_user()
    bot.respond(update, "Here is a contact for you.", success_callback=success_send_message,
                failure_callback=failure_send_message)
    contact_message = ContactMessage(name="test contact", emails=["test@test.com"], phones=["09123456789"])
    bot.send_message(contact_message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message)
    dispatcher.finish_conversation(update)


if __name__ == '__main__':
    updater.run()
