#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Voice and Photo simple conversation with bot."""
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
    message = TextMessage("Hi , nice to meet you :)"
                          "\nif you want to see my photo,"
                          "\nsend me a *voice*")
    user_peer = update.get_effective_user()
    kwargs = {'update': update}
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(VoiceFilter(), get_voice),
                                                                MessageHandler(DefaultFilter(), skip_voice)])


@dispatcher.message_handler(VoiceFilter())
def get_voice(bot, update):
    user_peer = update.get_effective_user()
    kwargs = {'update': update}

    def success_send_photo_message(result, user_data):
        message = TextMessage("Hahahaha! It's me."
                              "\nNow It's your turn."
                              "\nSend me your photo:")
        bot.send_message(message, user_peer, success_callback=success_send_message,
                         failure_callback=failure_send_message, kwargs=kwargs)
        dispatcher.register_conversation_next_step_handler(update, MessageHandler(PhotoFilter(), finish_conversion))

    bot.send_photo(user_peer=user_peer, image="./assets/happy-bot.jpeg", caption_text="caption comes here!",
                   name="bale.jpg", file_storage_version=1, mime_type="image/jpeg",
                   success_callback=success_send_photo_message)


def skip_voice(bot, update):
    message = TextMessage("So, It seems you don't like to send me 'Hello' voice!"
                          "\nplease just give me your photo.")
    user_peer = update.get_effective_user()
    kwargs = {'update': update}
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(PhotoFilter(), finish_conversion))


def finish_conversion(bot, update):
    user_peer = update.get_effective_user()
    photo_message_given = update.get_effective_message()
    kwargs = {'update': update}
    bot.reply(update, photo_message_given, success_callback=success_send_message, failure_callback=failure_send_message,
              kwargs=kwargs)
    message = TextMessage("Thanks \ngoodbye ;)")
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message,
                     kwargs=kwargs)
    dispatcher.finish_conversation(update)


if __name__ == '__main__':
    updater.run()
