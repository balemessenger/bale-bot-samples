import logging

from telegram import Bot
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

PHOTO = 0


def start(bot: Bot, update):
    update.message.reply_text(text="send a photo please")
    return PHOTO


def photo(bot, update):
    update.message.reply_photo(photo=update.message.photo[-1],
                               # photo="file_id",
                               # photo=open(file="file_path", mode='rb')
                               )
    return ConversationHandler.END


bot = Bot(token="Token",
          base_url="https://tapi.bale.ai/",
          base_file_url="https://tapi.bale.ai/file/")
updater = Updater(bot=bot)

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        PHOTO: [MessageHandler(filters=Filters.photo, callback=photo)],
    },

    fallbacks=[]
)

updater.dispatcher.add_handler(conversation_handler)

updater.start_polling(poll_interval=2)
# you can replace above line with commented below lines to use webhook instead of polling
# updater.start_webhook(listen=os.getenv('WEB_HOOK_IP', ""), port=int(os.getenv('WEB_HOOK_PORT', "")),
#                       url_path=os.getenv('WEB_HOOK_PATH', ""))
# updater.bot.set_webhook(url="{}{}".format(os.getenv('WEB_HOOK_DOMAIN', ""), os.getenv('WEB_HOOK_PATH', "")))
updater.idle()
