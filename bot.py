from telegram.ext import Updater, MessageHandler, Filters

TOKEN = "7603313779:AAHpodzsNXjRZSfG1Ju9qJJDnDvQzL0AxH0"  # Замените на токен от @BotFather
YOUR_CHAT_ID = -1002639758531  # Узнайте через @getmyid_bot

def forward(update, context):
    update.message.forward(chat_id=YOUR_CHAT_ID)

updater = Updater(TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.all, forward))
updater.start_polling()
print("Бот работает! 🚀")
updater.idle()
