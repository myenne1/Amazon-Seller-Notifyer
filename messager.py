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

def handle_incoming_request(request):
    if "/price" in request:
        handle_price(request)
    else:
        send_telegram_message("couldn't process request")
        return 0

def handle_price(request: str):
    split_text = request.split()
    asin = split_text[1]
    try:
        new_price = float(split_text[2])
    except Exception as e:
        send_telegram_message("New price must be a float")
    
    set_price(new_price, asin)
    send_telegram_message(f"Price for {asin} set to {new_price}")