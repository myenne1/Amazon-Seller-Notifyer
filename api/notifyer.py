from flask import Flask, jsonify, request
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
def telegram_bot(request: request):
    update = request.get_json(silent=True)
    
    if not update or "message" not in update:
        return {"ok": True}
    
    message = update["message"]
    handle_incoming_request(message)
    
    return {"ok": True}