"""Doc simple conversion with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater
import datetime

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


def final_download_success(result, user_data):
    print("download was successful : ", result)

    stream = user_data.get("byte_stream", None)
    now = str(datetime.datetime.now().time().strftime('%Y-%m-%d_%H:%M:%f'))
    print(type(stream))

    with open("../files/doc_downloaded_" + now, "wb") as file:
        file.write(stream)
        file.close()


@dispatcher.command_handler(["/start"])
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
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(DocumentFilter(), download_file))


def download_file(bot, update):
    def success_get_download_url(result, user_data):
        print("success : ", result)
        url = str(result.body.url)
        url_link = TextMessage("Link of downloaded photo:\n(Note : this link is for limited time)\n" + url)
        bot.send_message(url_link, user_peer, success_callback=success, failure_callback=failure)

    message = TextMessage("Downloading ... ")
    user_peer = update.get_effective_user()
    user_id = update.body.sender_user.peer_id
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    file_id = update.body.message.file_id
    bot.download_file(file_id=file_id, user_id=user_id, file_type="file", success_callback=final_download_success,
                      failure_callback=failure)
    bot.get_file_download_url(file_id, user_id, "file", success_callback=success_get_download_url,
                              failure_callback=failure)
    message = TextMessage("Download was successful\n"
                          "use below command to upload that document we already downloaded\n"
                          "[/upload](send:/upload)")
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, CommandHandler("upload", upload_file))


def upload_file(bot, update):
    def file_upload_success(result, user_data):
        """Its the link of upload photo but u cant see anything with it because you need to take a token from server.
            actually this link is just for uploading a file not download. If you want to download this file you should
            use get_file_download_url() and take a token from server.
        """
        print("upload was successful : ", result)
        print(user_data)
        url = user_data.get("url", None)
        url_message = TextMessage(url)
        bot.send_message(url_message, user_peer, success_callback=success, failure_callback=failure)

    message = TextMessage("Uploading ...")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    bot.upload_file(file="../files/upload_file_test.jpeg", file_type="file", success_callback=file_upload_success,
                    failure_callback=failure)

    message = TextMessage("Uploading is finish.\nyou can try this link and see nothing show to you\n"
                          "finish conversion with below command\n"
                          "[/finish](send:/finish)")
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)

    dispatcher.register_conversation_next_step_handler(update, CommandHandler("/finish", finish_conversion))


def finish_conversion(bot, update):
    message = TextMessage("Thanks \ngoodbye ;)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
