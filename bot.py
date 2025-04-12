from telegram.ext import Updater, MessageHandler
from telegram.ext import filters  # Новое название вместо Filters!
from flask import Flask
import os

app = Flask(__name__)

TOKEN = "7603313779:AAE6tsonkxwULPaMWqam8HGX829naYTAs3w"
CHAT_ID = -1002639758531
PORT = int(os.environ.get('PORT', 10000))

@app.route('/')
def home():
    return "Бот активен", 200

def forward(update, context):
    update.message.forward(chat_id=CHAT_ID)

if __name__ == '__main__':
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(filters.ALL, forward))  # Используем filters.ALL
    
    app.run(host='0.0.0.0', port=PORT)
    updater.start_polling()
    updater.idle()
