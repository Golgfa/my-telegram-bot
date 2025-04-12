from telegram.ext import Updater, MessageHandler, Filters
from flask import Flask  # Добавляем веб-сервер
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот активен", 200

TOKEN = os.getenv('7603313779:AAHpodzsNXjRZSfG1Ju9qJJDnDvQzL0AxH0')
CHAT_ID = os.getenv('-1002639758531')

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

def forward(update, context):
    update.message.forward(chat_id=CHAT_ID)

if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Настройка бота
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, forward))
    
    updater.start_polling(
        drop_pending_updates=True,
        timeout=20,
        clean=True
    )
    print("🤖 Бот запущен с веб-сервером")
    updater.idle()
