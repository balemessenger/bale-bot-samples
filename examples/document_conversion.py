"""Text simple conversion with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater
import datetime

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
    print("upload was successful : ", result)
    print(user_data)
    # file_id = user_data.get("file_id", None)
    # user_id = user_data.get("user_id", None)
    # url = user_data.get("url", None)
    # dup = user_data.get("dup", None)

    # bot.download_file(file_id=file_id, user_id=user_id, file_type="file",
    #                   success_callback=final_download_success,
    #                   failure_callback=failure)


def final_download_success(result, user_data):
    print("download was successful : ", result)

    stream = user_data.get("byte_stream", None)
    now = str(datetime.datetime.now().time().strftime('%Y-%m-%d_%H:%M:%f'))
    print(type(stream))

    with open("../documents/doc_downloaded_" + now, "wb") as file:
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
    message = TextMessage("Downloading ... ")
    user_peer = update.get_effective_user()
    user_id = update.body.sender_user.peer_id
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    file_id = update.body.message.file_id
    bot.download_file(file_id=file_id, user_id=user_id, file_type="file", success_callback=final_download_success,
                      failure_callback=failure)
    message = TextMessage("Download was successful\n"
                          "use below command to upload that document we already downloaded\n"
                          "[/upload](send:/upload @first_bot/)")
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, CommandHandler("upload", upload_file))


def upload_file(bot, update):
    message = TextMessage("Uploading ...")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    bot.upload_file(file="../documents/upload_file", file_type="file", success_callback=file_upload_success,
                    failure_callback=failure)
    message = TextMessage("Uploading is finish.\nyou can try it with this link\n"
                          "(Note : this link is for limited time)")
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)

    dispatcher.register_conversation_next_step_handler(update, MessageHandler(VoiceFilter(), finish_conversion))


def finish_conversion(bot, update):
    message = TextMessage("Thanks \ngoodbye ;)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
