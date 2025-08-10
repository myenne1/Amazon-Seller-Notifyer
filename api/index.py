from flask import Flask, jsonify
from amz import poll_and_notify

app = Flask(__name__)

@app.get("/notifyer")
def run():
    processed = poll_and_notify()
    return jsonify({"ok": True, "processed": processed})
