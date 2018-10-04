"""Purchase message simple conversation with bot."""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.models.messages.banking.money_request_type import MoneyRequestType
from balebot.updater import Updater
from balebot.utils.logger import Logger

# Bale Bot Authorization Token
updater = Updater(token="PUT YOUR TOKEN HERE",
                  loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher
my_logger = Logger.get_logger()  # Create a logger and name it my_logger


def success_send_message(response, user_data):
    kwargs = user_data['kwargs']
    update = kwargs["update"]
    user_peer = update.get_effective_user()
    my_logger.info("Your message has been sent successfully.", extra={"user_id": user_peer.peer_id, "tag": "info"})


def failure_send_message(response, user_data):
    kwargs = user_data['kwargs']
    update = kwargs["update"]
    user_peer = update.get_effective_user()
    my_logger.error("Sending message has been failed", extra={"user_id": user_peer.peer_id, "tag": "error"})


@dispatcher.command_handler(["/start"])
def conversation_starter(bot, update):
    message = TextMessage("Hi , nice to meet you :)\nplease send me a photo")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(PhotoFilter(), purchase_message))


@dispatcher.message_handler(PhotoFilter())
def purchase_message(bot, update):
    message = update.get_effective_message()
    user_peer = update.get_effective_user()
    first_purchase_message = PurchaseMessage(msg=message, account_number=6037991067471130, amount=10,
                                             money_request_type=MoneyRequestType.normal)
    bot.send_message(first_purchase_message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message)
    dispatcher.finish_conversation(update)


updater.run()
