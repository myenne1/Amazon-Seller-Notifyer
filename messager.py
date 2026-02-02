from os import setpriority
import requests
from config import settings
from supa import asin_exists, set_price

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID


def send_telegram_message(msg: str, chat_id: int = TELEGRAM_CHAT_ID):
    """Send a message to Telegram; default to the configured chat unless overridden."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": msg,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response


def handle_incoming_request(update: dict):
    """
    Process a Telegram webhook update. Extracts the inner message object safely.
    """
    if not update:
        send_telegram_message("No update payload received.")
        return

    # Telegram delivers messages under `message` (or `edited_message`, etc.)
    message = update.get("message") or update.get("edited_message")
    if not message:
        send_telegram_message("No message found in update.")
        return

    chat_id = message.get("chat", {}).get("id", TELEGRAM_CHAT_ID)
    message_id = message.get("message_id")
    is_bot = message.get("from", {}).get("is_bot", False)
    text = (message.get("text") or "").strip()

    print(f"id: {message_id}")
    print(f"bot: {is_bot}")
    print(f"text: {text}")

    if not text:
        send_telegram_message("Empty message received.", chat_id)
        return

    if text.startswith("/price"):
        handle_price(chat_id, text)
        return

    send_telegram_message("Couldn't process request. Try: /price <ASIN> <PRICE>", chat_id)


def handle_price(chat_id: int, text: str):
    split_text = text.split()

    if len(split_text) != 3:
        send_telegram_message(
            "Usage: /price <ASIN> <PRICE>\nExample: /price B0DC8R7LT2 42.95",
            chat_id,
        )
        return

    if split_text[1].strip() == "36000":
        asin = "B0F8LMQN9P"
        
    elif split_text[1].strip() == "24000":
        asin = 'B0DC8R7LT2'
    
    if not asin_exists(asin):
        send_telegram_message("Could not find asin.", chat_id)
        
    price_str = split_text[2].strip()

    try:
        new_price = float(price_str)
    except ValueError:
        send_telegram_message("New price must be a number. Example: 42.95", chat_id)
        return

    if new_price <= 0:
        send_telegram_message("Price must be greater than 0.", chat_id)
        return

    set_price(new_price, asin)
    send_telegram_message(f"Price for {asin} set to {new_price:.2f}", chat_id)
