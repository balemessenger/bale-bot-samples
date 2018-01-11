"""Template simple conversion with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater

# A token you give from BotFather when you create your bot set below
updater = Updater(token="114d273b48f04cd7c3be657328d2aa5521dae020",
                  loop=asyncio.get_event_loop())
bot = updater.bot
dispatcher = updater.dispatcher


def success(result, user_data):
    print("success : ", result)
    print(user_data)


def failure(result, user_data):
    print("failure : ", result)
    print(user_data)


@dispatcher.command_handler(["talk"])
def conversation_starter(bot, update):
    message = TextMessage("Hi , come try a interesting message :)\nplease tell me a [yes, no] question.")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), ask_question))


def ask_question(bot, update):
    user_peer = update.get_effective_user()
    my_message = TextMessage("Your Template Message created!")
    bot.send_message(my_message, user_peer, success_callback=success, failure_callback=failure)
    message = str(update.body.message.text)
    general_message = TextMessage(message)
    btn_list = [TemplateMessageButton(text="yes", value="yes", action=0),
                TemplateMessageButton(text="no", value="no", action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(TemplateResponseFilter(keywords=["yes"]),
                                                                       positive_answer),
                                                        MessageHandler(TemplateResponseFilter(keywords=["no"]),
                                                                       negative_answer)])


def positive_answer(bot, update):
    message = TextMessage("Your answer is 'YES' \n"
                          "end the conversion with below command: \n"
                          "[/end](send:/end @first_bot/)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, CommandHandler("end", finish_conversion))


def negative_answer(bot, update):
    message = TextMessage("Your answer is 'NO' \n"
                          "Write a new question or end the conversion with below command: \n"
                          "[/end](send:/end @first_bot/)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TextFilter(), ask_question),
                                                                CommandHandler("end", finish_conversion)])


def finish_conversion(bot, update):
    message = TextMessage("Thanks \ngoodbye ;)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
