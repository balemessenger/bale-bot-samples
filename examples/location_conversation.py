"""Location message conversation with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.models.messages.location_message import LocationMessage
from balebot.updater import Updater
import datetime

# Bale Bot Authorization Token
updater = Updater(token="PUT YOUR TOKEN HERE",
                  loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher


def success(response, user_data):
    print("success : ", response)
    print(user_data)


def failure(response, user_data):
    print("failure : ", response)
    print(user_data)


@dispatcher.message_handler(filters=LocationFilter())
def conversation_starter(bot, update):
    user_peer = update.get_effective_user()
    general_message = TextMessage("Hi ,Are you hungry?")
    btn_list = [TemplateMessageButton(text="yes", value="yes", action=0),
                TemplateMessageButton(text="no", value="no", action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TemplateResponseFilter(keywords=["yes"]),
                                                                               find_location),
                                                                MessageHandler(TemplateResponseFilter(keywords=["no"]),
                                                                               no_thanks)])


def no_thanks(bot, update):
    bot.reply(update, "It's Ok.", success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


def find_location(bot, update):
    user_peer = update.get_effective_user()
    bot.reply(update, "Here is a good restaurant sir.", success_callback=success, failure_callback=failure)
    # Make a location from LocationMessage and send it.
    location_message = LocationMessage(longitude="51.41714821748457", latitude="35.73122955392002")
    bot.send_message(location_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
