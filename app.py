
from flask import Flask, request, render_template_string, jsonify
import os
import secrets
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

BOT_TOKEN = "7810937535:AAGgsmOSwXTZ-riH5tEWLMUb_azG5K5FCWQ"
BOT_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

TOKENS = {}

def generate_token(user_id):
    token = secrets.token_urlsafe(16)
    expiration = datetime.utcnow() + timedelta(hours=1)
    TOKENS[token] = {"user_id": user_id, "expires": expiration}
    return token

def validate_token(token):
    token_data = TOKENS.get(token)
    if not token_data:
        return False
    if datetime.utcnow() > token_data["expires"]:
        del TOKENS[token]
        return False
    return True

@app.route("/")
def home():
    return "Naksir Predictions API is live"

@app.route("/generate-token", methods=["GET"])
def generate_token_route():
    user_id = request.args.get("user_id", "anonymous")
    token = generate_token(user_id)
    return {"token": token}

@app.route("/validate-token", methods=["GET"])
def validate_token_route():
    token = request.args.get("token")
    return {"valid": validate_token(token)}

@app.route("/soccer")
def soccer():
    token = request.args.get("token")
    if not token or not validate_token(token):
        return "<h2 style='color:red;'>❌ Unauthorized. Please access via Telegram Mini App.</h2>", 401

    html = '''
    <html>
    <head>
        <title>Naksir Premium Predictions</title>
        <meta http-equiv="refresh" content="60">
        <style>
            body { font-family: Arial; text-align: center; padding: 20px; }
            .loader { width: 50px; height: 50px; background: url('https://i.imgur.com/6RMhx.gif') no-repeat center; background-size: contain; margin: 20px auto; }
        </style>
    </head>
    <body>
        <h2>⚽️ Naksir Premium Predictions</h2>
        <div class="loader"></div>
        <p><b>📅 Competition:</b> Italy Serie A</p>
        <p><b>🏟 Match:</b> Juventus vs Genoa</p>
        <p><b>🎯 Total Goals (Over/Under 2.5):</b><br>Over: 40%<br>Under: 60%</p>
        <p><b>📘 BTTS:</b><br>Yes: 35%<br>No: 65%</p>
        <p><b>⏱️ Match Outcome:</b><br>Team 1 Win: 70%<br>Draw: 20%<br>Team 2 Win: 10%</p>
        <p><b>💡 Highest Probability Bet:</b><br><span style='color:blue;'>Juventus to win 70%</span></p>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route("/create-invoice", methods=["POST"])
def create_invoice():
    payload = {
        "title": "Naksir Premium Tip",
        "description": "Access today's top soccer prediction",
        "payload": "{}",
        "provider_token": "",
        "currency": "XTR",
        "prices": [{"amount": 50, "label": "Premium Tip"}],
    }

    response = requests.post(f"{BOT_API}/createInvoiceLink", json=payload)
    data = response.json()

    if not data.get("ok"):
        return jsonify({"error": "Failed to create invoice"}), 500

    return jsonify({"invoiceLink": data["result"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
