import os
from telegram.ext import Updater, MessageHandler, Filters
from flask import Flask
import threading
import logging
import time

# Конфигурация
TOKEN = "7603313779:AAE6tsonkxwULPaMWqam8HGX829naYTAs3w"
CHAT_ID = -1002639758531
PORT = 10000

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Бот работает ✅", 200

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

def forward_message(update, context):
    try:
        update.message.forward(chat_id=CHAT_ID)
        logger.info(f"Переслано сообщение от @{update.message.from_user.username}")
    except Exception as e:
        logger.error(f"Ошибка: {e}")

def start_bot():
    retry_count = 0
    max_retries = 3
    
    while retry_count < max_retries:
        try:
            updater = Updater(TOKEN, request_kwargs={
                'read_timeout': 30,
                'connect_timeout': 30,
                'pool_timeout': 30
            })
            
            dp = updater.dispatcher
            dp.add_handler(MessageHandler(Filters.all, forward_message))
            
            updater.start_polling(
                drop_pending_updates=True,
                timeout=30,
                poll_interval=3,
                bootstrap_retries=-1
            )
            logger.info("Бот успешно запущен")
            return updater
        except Exception as e:
            retry_count += 1
            logger.warning(f"Попытка {retry_count}/{max_retries}. Ошибка: {e}")
            if retry_count < max_retries:
                time.sleep(10)
    
    logger.error("Не удалось запустить бота после нескольких попыток")
    raise RuntimeError("Max retries exceeded")

if __name__ == '__main__':
    # Запуск Flask в фоне
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Основной поток с ботом
    try:
        updater = start_bot()
        updater.idle()
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
