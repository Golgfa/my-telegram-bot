from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from flask import Flask
import os
import asyncio
from threading import Thread

app = Flask(__name__)

TOKEN = os.getenv('TOKEN', '7603313779:AAE6tsonkxwULPaMWqam8HGX829naYTAs3w')
CHAT_ID = int(os.getenv('CHAT_ID', '-1002639758531'))
PORT = int(os.getenv('PORT', 10000))

@app.route('/')
def home():
    return "Бот активен", 200

async def forward(update: Update, context):
    await update.message.forward(chat_id=CHAT_ID)

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, forward))
    
    loop.run_until_complete(application.run_polling())

if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Запускаем бота в главном потоке
    run_bot()
