from os import setpriority
import requests
from config import settings
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from supa import set_price

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID

def send_telegram_message(msg: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response

def handle_incoming_request(message: dict):
    id = message["message_id"]
    is_bot = message["is_bot"]
    new_text = message["text"]
    print(f"id: {id}")
    print(f"bot: {is_bot}")
    print(f"text: {new_text}")
    
    text = (message.get("text") or "").strip()

    if not text:
        send_telegram_message("Empty message received.")
        return

    if text.startswith("/price"):
        handle_price(text)
        return

    send_telegram_message("Couldn't process request. Try: /price <ASIN> <PRICE>")

def handle_price(chat_id: int, text: str):
    split_text = text.split()

    if len(split_text) != 3:
        send_telegram_message(
            chat_id,
            "Usage: /price <ASIN> <PRICE>\nExample: /price B0DC8R7LT2 42.95"
        )
        return

    asin = split_text[1].strip()
    price_str = split_text[2].strip()

    try:
        new_price = float(price_str)
    except ValueError:
        send_telegram_message(chat_id, "New price must be a number. Example: 42.95")
        return

    if new_price <= 0:
        send_telegram_message(chat_id, "Price must be greater than 0.")
        return

    set_price(new_price, asin)
    send_telegram_message(chat_id, f"Price for {asin} set to {new_price:.2f}")
