import telebot
import os
import schedule
import time
from flask import Flask, request

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
CHAT_ID = os.getenv("MY_CHAT_ID")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive"

@app.route("/" + API_TOKEN, methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.reply_to(message, "я - тут!")

def send_morning_message():
    bot.send_message(CHAT_ID, "доброго ранку!")

schedule.every().day.at("06:00").do(send_morning_message)  # 06:00 UTC = 08:00 Київ

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

import threading
threading.Thread(target=run_scheduler).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
