"""Contact message conversation with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import *
from balebot.models.messages.contact_message import ContactMessage
from balebot.updater import Updater

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


@dispatcher.message_handler(filters=ContactFilter())  # filter text the client enter to bot
def conversation_starter(bot, update):
    user_peer = update.get_effective_user()
    general_message = TextMessage("Hi ,I receive your contact, Can I send you a contact too?")
    btn_list = [TemplateMessageButton(text="yes", value="yes", action=0),
                TemplateMessageButton(text="no", value="no", action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, [MessageHandler(TemplateResponseFilter(keywords=["yes"]),
                                                                               send_contact),
                                                                MessageHandler(TemplateResponseFilter(keywords=["no"]),
                                                                               no_thanks)])


def no_thanks(bot, update):
    bot.reply(update, "It's Ok.", success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


def send_contact(bot, update):
    user_peer = update.get_effective_user()
    bot.respond(update, "Here is a contact for you.", success_callback=success, failure_callback=failure)
    contact_message = ContactMessage(name="test contact", emails=["test@test.com"], phones=["09123456789"])
    bot.send_message(contact_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation(update)


updater.run()
