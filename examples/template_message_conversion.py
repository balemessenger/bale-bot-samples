"""Template simple conversion with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater

# A token you give from BotFather when you create your bot set below
updater = Updater(token="PUT YOUR TOKEN HERE",
                  loop=asyncio.get_event_loop())
bot = updater.bot
dispatcher = updater.dispatcher


def success(response, user_data):
    print("success : ", response)
    print(user_data)


def failure(response, user_data):
    print("failure : ", response)
    print(user_data)


@dispatcher.command_handler(["/start"])
def conversation_starter(bot, update):
    message = TextMessage("*Hi , come try a interesting message* \nplease tell me a *yes-no* question.")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), ask_question))


def ask_question(bot, update):
    user_peer = update.get_effective_user()
    my_message = TextMessage("*Your Template Message created!*")
    bot.send_message(my_message, user_peer, success_callback=success, failure_callback=failure)
    # Set client message as general message of a template message
    general_message = update.get_effective_message()
    # Create how many buttons you like with TemplateMessageButton class
    btn_list = [TemplateMessageButton(text="yes", value="yes", action=0),
                TemplateMessageButton(text="no", value="no", action=0)]
    # Create a Template Message
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(TemplateResponseFilter(keywords=["yes"]),
                                                                       positive_answer),
                                                        MessageHandler(TemplateResponseFilter(keywords=["no"]),
                                                                       negative_answer)])


# Use when answer is 'yes'
def positive_answer(bot, update):
    message = TextMessage("*Your have answered 'yes'* \n"
                          "end the conversion with below command: \n"
                          "[/end](send:/end)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    # Use CommandHandler to handle a command which is sent by client
    dispatcher.register_conversation_next_step_handler(update, CommandHandler("/end", finish_conversion))


# Use when answer is 'no'
def negative_answer(bot, update):
    message = TextMessage("*Your have answered 'no'* \n"
                          "Write a new question or end the conversion with below command: \n"
                          "[/end](send:/end)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [CommandHandler("/end", finish_conversion)])


def finish_conversion(bot, update):
    message = TextMessage("*Thanks* \ngoodbye ;)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    # Finish conversation
    dispatcher.finish_conversation(update)


updater.run()
