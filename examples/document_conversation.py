#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Doc simple conversation with bot."""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.updater import Updater
from balebot.utils.logger import Logger
import datetime

# Bale Bot Authorization Token
updater = Updater(token="TOKEN",
                  loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher

# Enable logging
logger = Logger.get_logger()


def success_send_message(response, user_data):
    logger.info("Your message has been sent successfully.", extra={"tag": "info"})


def failure_send_message(response, user_data):
    logger.error("Sending message has been failed", extra={"tag": "error"})


@dispatcher.command_handler(["/start"])
def conversation_starter(bot, update):
    message = TextMessage("Hi , nice to meet you :)\nplease send me a contact.")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(ContactFilter(), ask_contact),
                                                                MessageHandler(DefaultFilter(), no_contact)])


def ask_contact(bot, update):
    user_peer = update.get_effective_user()
    bot.reply(update, "its a contact", success_callback=success_send_message, failure_callback=failure_send_message)
    message = TextMessage("Thanks \nplease send a document you want")
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(DocumentFilter(), download_file))


def no_contact(bot, update):
    message = TextMessage("So, it seems you don't have any contact.\n you can try a upload a document here"
                          "\n now send me a document")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(DocumentFilter(), download_file))


def download_file(bot, update):
    user_peer = update.get_effective_user()
    user_id = update.body.sender_user.peer_id
    message = TextMessage("Downloading ... ")
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message)
    file_id = update.get_effective_message().file_id

    def final_download_success(result, user_data):
        logger.info("download was successful", extra={"tag": "info"})
        stream = user_data.get("byte_stream", None)
        dispatcher.set_conversation_data(update, "stream", stream)
        now = str(datetime.datetime.now().time().strftime('%Y-%m-%d_%H:%M:%f'))
        with open("doc_downloaded_" + now, "wb") as file:
            file.write(stream)
            file.close()

    def final_download_failure(result, user_data):
        logger.error("download was failure", extra={"tag": "error"})

    bot.download_file(file_id=file_id, user_id=user_id, file_type="file", success_callback=final_download_success,
                      failure_callback=final_download_failure)

    def get_download_url_success(result, user_data):
        logger.info("get download url successful", extra={"tag": "info"})
        url = str(result.body.url)
        logger.info("Link of downloaded photo:\n(Note : this link is for limited time)\n" + url, extra={"tag": "info"})

    def get_download_url_failure(result, user_data):
        logger.error("get download url failure", extra={"tag": "error"})

    bot.get_file_download_url(file_id, user_id, "file", success_callback=get_download_url_success,
                              failure_callback=get_download_url_failure)
    message = TextMessage("Download was successful\n"
                          "use below command to upload the document we already downloaded\n"
                          "[/upload](send:/upload)")
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=final_download_success)
    dispatcher.register_conversation_next_step_handler(update, CommandHandler("upload", upload_file))


def upload_file(bot, update):
    def file_upload_success(result, user_data):
        """Its the link of upload photo but u cant see anything with it because you need to take a token from server.
            actually this link is just for uploading a file not download. If you want to download this file you should
            use get_file_download_url() and take a token from server.
        """
        logger.info("file upload success", extra={"tag": "info"})

    def file_upload_failure(result, user_data):
        logger.error("file upload failure", extra={"tag": "error"})

    message = TextMessage("Uploading ...")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message)
    stream = dispatcher.get_conversation_data(update, "stream")
    bot.upload_file(file=stream, file_type="file", success_callback=file_upload_success,
                    failure_callback=file_upload_failure)

    message = TextMessage("Uploading is finish.\nyou can try this link and see nothing show to you\n"
                          "finish conversion with below command\n"
                          "[/finish](send:/finish)")
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message)

    dispatcher.register_conversation_next_step_handler(update, CommandHandler("/finish", finish_conversion))


def finish_conversion(bot, update):
    message = TextMessage("Thanks \ngoodbye ;)")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success_send_message, failure_callback=failure_send_message)
    dispatcher.finish_conversation(update)


if __name__ == '__main__':
    updater.run()
