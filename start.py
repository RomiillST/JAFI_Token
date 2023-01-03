from telegram.ext import Updater,MessageHandler, Filters, CommandHandler
from const import TOKEN
from func import *

upd = Updater(token=TOKEN, workers=4)
dis = upd.dispatcher
dis.add_handler(CommandHandler(command='start', callback=start))
dis.add_handler(CommandHandler(command='ultaaa', callback=imba))
dis.add_handler(MessageHandler(filters=Filters.text, callback=text_answer))
upd.start_polling(drop_pending_updates=True)
upd.idle()
