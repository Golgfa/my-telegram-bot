from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from flask import Flask
import os
import asyncio

app = Flask(__name__)

TOKEN = os.getenv('TOKEN', '7603313779:AAE6tsonkxwULPaMWqam8HGX829naYTAs3w')
CHAT_ID = int(os.getenv('CHAT_ID', '-1002639758531'))
PORT = int(os.getenv('PORT', 10000))

@app.route('/')
def home():
    return "Бот активен", 200

async def forward(update: Update, context):
    await update.message.forward(chat_id=CHAT_ID)

async def start_bot():
    # Создаем Application вместо Updater
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчик
    application.add_handler(MessageHandler(filters.ALL, forward))
    
    # Запускаем polling
    await application.run_polling()

if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    from threading import Thread
    Thread(target=app.run, kwargs={'host':'0.0.0.0','port':PORT}, daemon=True).start()
    
    # Запускаем бота
    asyncio.run(start_bot())
