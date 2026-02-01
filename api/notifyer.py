from requests import Request
from flask import Flask, jsonify
from amz import poll_and_notify
from messager import handle_incoming_request, send_telegram_message
from supa import get_price_setting

app = Flask(__name__)

@app.get("/")
def run():
    processed = poll_and_notify()
    return jsonify({"ok": True, "processed": processed})

@app.get("/health")
def health():
    return {"ok": True, "service": "amazon-notifier"}

@app.post("/api/telegram")
def telegram_bot(request: Request):
    handle_incoming_request(request)