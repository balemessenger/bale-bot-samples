"""Text simple conversion with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.updater import Updater

# A token you give from BotFather when you create your bot set below
updater = Updater(token="PUT YOUR TOKEN HERE",
                  loop=asyncio.get_event_loop())
bot = updater.bot
dispatcher = updater.dispatcher


def success(response, user_data):
    # Check if there is any user data or not
    if user_data:
        user_data = user_data['kwargs']
        user_peer = user_data["user_peer"]
        message = user_data["message"]
        print("message : " + message.text + "\nuser id : ", user_peer.peer_id)
    print("success : ", response)


def failure(response, user_data):
    print("user_data : ", user_data)
    print("failure : ", response)


@dispatcher.command_handler(["/start"])
def conversation_starter(bot, update):
    message = TextMessage("*Hi , nice to meet you*\nplease tell me your name.")
    # Get client user object by a function called (get_effective_user)
    user_peer = update.get_effective_user()
    # Set any user data in kwargs mode
    kwargs = {"message": message, "user_peer": user_peer}
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
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
    kwargs = {"message": message, "user_peer": user_peer}
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure, kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(update,
                                                       # Set Regex pattern for TextFilter
                                                       MessageHandler(TextFilter(pattern="^[0-9]+$"),
                                                                      finish_conversion))


def skip_name(bot, update):
    message = TextMessage("*So, you don't want to tell your name!*\nplease just tell me your age")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    no_name = "no name"
    dispatcher.set_conversation_data(update=update, key="name", value=no_name)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), finish_conversion))


def finish_conversion(bot, update):
    message = TextMessage("*Thanks!*\ngoodbye ;)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    name = dispatcher.get_conversation_data(update, key="name")
    age = update.get_effective_message().text
    output = TextMessage("*Name:* " + name + "\n" + "*Age:* " + age)
    bot.send_message(output, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
