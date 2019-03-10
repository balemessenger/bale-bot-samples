#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Purchase message simple conversation with bot."""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.models.messages.banking.money_request_type import MoneyRequestType
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
    message = TextMessage("Hi , nice to meet you :)\nplease send me a photo")
    user_peer = update.get_effective_user()
    kwargs = {'update': update}
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(PhotoFilter(), purchase_message))


@dispatcher.message_handler(PhotoFilter())
def purchase_message(bot, update):
    message = update.get_effective_message()
    user_peer = update.get_effective_user()
    purchase_message = PurchaseMessage(msg=message, account_number=6037991067471130, amount=10,
                                       money_request_type=MoneyRequestType.normal)
    kwargs = {'update': update}
    bot.send_message(purchase_message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message, kwargs=kwargs)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(BankMessageFilter())
def handle_receipt(bot, update):
    bank_message = update.get_effective_message()
    user_peer = update.get_effective_user()
    receipt = bank_message.get_receipt()
    kwargs = {'update': update}
    message = TextMessage("your payment receipt received with trace Number: {}".format(receipt.traceNo))
    bot.send_message(message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message, kwargs=kwargs)
    logger.info(receipt, extra={"tag": "info"})
    logger.info(receipt.payer, receipt.msgUID, extra={"tag": "info"})


if __name__ == '__main__':
    updater.run()
