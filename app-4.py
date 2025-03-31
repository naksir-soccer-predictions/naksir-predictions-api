
from flask import Flask, request, jsonify, render_template_string, redirect
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

ADMIN_PASSWORD = "naksir2025"
PREDICTION_FILE = "prediction.json"

TOKENS = {}

def generate_token(user_id):
    import secrets
    token = secrets.token_urlsafe(16)
    TOKENS[token] = {"user_id": user_id, "expires": datetime.utcnow() + timedelta(minutes=30)}
    return token

def validate_token(token):
    data = TOKENS.get(token)
    if not data or datetime.utcnow() > data["expires"]:
        return False
    return True

@app.route("/")
def home():
    return "Naksir Predictions API is live"

@app.route("/generate-token")
def generate_token_route():
    user_id = request.args.get("user_id", "anonymous")
    token = generate_token(user_id)
    return jsonify({"token": token})

@app.route("/validate-token")
def validate_token_route():
    token = request.args.get("token")
    return jsonify({"valid": validate_token(token)})

@app.route("/soccer")
def soccer():
    token = request.args.get("token")
    if not token or not validate_token(token):
        return "<h2 style='color:red;'>❌ Unauthorized. Please access via Telegram Mini App.</h2>", 401

    try:
        with open(PREDICTION_FILE) as f:
            p = json.load(f)
    except:
        return "<h2 style='color:red;'>No prediction available</h2>", 500

    html = f"""
    <html><head><title>Naksir Predictions</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
    <body style='font-family: Arial; padding:20px;'>
    <h2>⚽️ Naksir Premium Predictions ({p.get("date", "")})</h2>
    <p><b>Competition:</b> {p.get("competition", "")}</p>
    <p><b>Match:</b> {p.get("match", "")}</p>
    <p><b>Total Goals (Over/Under 2.5):</b><br>Over: {p.get("over", "")}%<br>Under: {p.get("under", "")}%</p>
    <p><b>BTTS:</b><br>Yes: {p.get("btts_yes", "")}%<br>No: {p.get("btts_no", "")}%</p>
    <p><b>Match Outcome:</b><br>Team 1 Win: {p.get("win1", "")}%<br>Draw: {p.get("draw", "")}%<br>Team 2 Win: {p.get("win2", "")}%</p>
    <p><b>💡 Highest Probability Bet:</b><br><span style='color:blue;'>{p.get("highest", "")}</span></p>
    </body></html>
    """
    return render_template_string(html)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        pw = request.args.get("pass")
        if pw != ADMIN_PASSWORD:
            return "Unauthorized", 401
        data = request.json
        with open(PREDICTION_FILE, "w") as f:
            json.dump(data, f)
        return jsonify({"status": "updated"})

    return '''
    <form method="post" action="/admin?pass=naksir2025" enctype="application/json">
    Use POST JSON data to update prediction.
    </form>
    '''

@app.route("/get")
def get_prediction():
    try:
        with open(PREDICTION_FILE) as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"error": "No data"}), 500

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.json
    # Ovde dodaj custom logiku za bot webhook ako želiš
    print("Received update:", update)
    return "", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
