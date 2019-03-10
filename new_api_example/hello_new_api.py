import logging

from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


def hello(bot, update):
    update.message.reply_text(
        'Hello {}. This message is from new api of Bale'.format(update.message.from_user.first_name))


updater = Updater(token='Token',
                  base_url="https://tapi.bale.ai/")

updater.dispatcher.add_handler(CommandHandler(command='hello', callback=hello))

updater.bot.delete_webhook()
updater.start_polling(poll_interval=2)
# you can replace above line with commented below lines to use webhook instead of polling
# updater.start_webhook(listen=os.getenv('WEB_HOOK_IP', ""), port=int(os.getenv('WEB_HOOK_PORT', "")),
#                       url_path=os.getenv('WEB_HOOK_PATH', ""))
# updater.bot.set_webhook(url="{}{}".format(os.getenv('WEB_HOOK_DOMAIN', ""), os.getenv('WEB_HOOK_PATH', "")))
updater.idle()
