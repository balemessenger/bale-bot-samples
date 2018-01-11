"""Voice and Photo simple conversion with bot
"""
import asyncio
import base64

from balebot.filters import *
from balebot.handlers import MessageHandler
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
    message = TextMessage("Hi , nice to meet you :)\nplease send me your photo.")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(PhotoFilter(), ask_photo),
                                                                MessageHandler(DefaultFilter(), skip_photo)])


def ask_photo(bot, update):
    user_peer = update.get_effective_user()

    def file_upload_success(result, user_data):
        """Its the link of upload photo but u cant see anything with it because you need to take a token from server.
            actually this link is just for uploading a file not download. If you want to download this file you should
            use get_file_download_url() and take a token from server.
        """
        print("upload was successful : ", result)
        print(user_data)
        file_id = str(user_data.get("file_id", None))
        access_hash = str(user_data.get("user_id", None))
        v_message = PhotoMessage(file_id=file_id, access_hash=access_hash, name="Bale", file_size='11337',
                                 mime_type="image/jpeg", caption_text=TextMessage(text="Bale"),
                                 file_storage_version=1, thumb=None)

        bot.send_message(v_message, user_peer, success_callback=success, failure_callback=failure)

    bot.upload_file(file="../documents/Bale", file_type="file", success_callback=file_upload_success,
                    failure_callback=failure)
    message = TextMessage("Thanks \nplease send a Hello voice message.")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(VoiceFilter(), finish_conversion))


def skip_photo(bot, update):
    message = TextMessage("So, you don't want to send me your photo !\nplease just give a Hello voice message.")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(VoiceFilter(), finish_conversion))


def finish_conversion(bot, update):
    user_peer = update.get_effective_user()
    v_message = update.get_effective_message()
    bot.reply(update, v_message, success_callback=success, failure_callback=failure)
    message = TextMessage("Thanks \ngoodbye ;)")
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
