"""Text simple conversion with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler,CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater
from balebot.utils.logger import Logger
from Config import Config

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


def file_upload_success(result, user_data):
    print("u success : ", result)
    print(user_data)


def final_download_success(result, user_data):
    print("d success : ", result)
    stream = user_data.get("byte_stream", None)
    print(type(stream))

    with open("hello", "wb") as file:
        file.write(stream)
        file.close()


@dispatcher.command_handler(["talk"])
def conversation_starter(bot, update):
    message = TextMessage("Hi , nice to meet you :)\nplease send me a contact.")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(ContactFilter(), ask_contact),
                                                                MessageHandler(DefaultFilter(), no_contact)])


def ask_contact(bot, update):
    user_peer = update.get_effective_user()
    bot.reply(update, "its a contact", success_callback=success, failure_callback=failure)
    message = TextMessage("Thanks \nplease send a document you want")
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(DocumentFilter(), download_file))


def no_contact(bot, update):
    message = TextMessage("So, it seems you don't have any contact.\n you can try a upload a document here"
                          "\n now send me a document")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(VoiceFilter(), finish_conversion))


def download_file(bot, update):
    message = TextMessage("we are downloading ... it with bot")
    user_peer = update.get_effective_user()
    user_id = update.body.sender_user.peer_id
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    file_id = update.body.message.file_id
    bot.download_file(file_id=file_id, user_id=user_id, file_type="file", success_callback=final_download_success,
                      failure_callback=failure)
    message = TextMessage("download was successful"
                          "use below command to upload that document we already downloaded"
                          " [/upload](send:/upload @first_bot/)")
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, CommandHandler("upload", upload_file))


def upload_file(bot, update):
    message = TextMessage("Download has finished successfully and we are uploading it now")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    bot.upload_file(file="contact", file_type="file", success_callback=file_upload_success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(VoiceFilter(), finish_conversion))


def finish_conversion(bot, update):
    message = TextMessage("Thanks \ngoodbye ;)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
