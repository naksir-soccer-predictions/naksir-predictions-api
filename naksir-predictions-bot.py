from flask import Flask, request, render_template_string, jsonify
import os
import secrets
from datetime import datetime, timedelta
import telegram

app = Flask(__name__)

TOKENS = {}

def generate_token(user_id):
    token = secrets.token_urlsafe(16)
    expiration = datetime.utcnow() + timedelta(minutes=10)
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

    html = """
    <html>
    <head>
        <title>Naksir Premium Predictions</title>
        <meta http-equiv="refresh" content="60">
        <style>
            body { font-family: Arial; text-align: center; padding: 20px; }
        </style>
    </head>
    <body>
        <h2>⚽️ Naksir Premium Predictions</h2>
        <p><b>📅 Competition:</b> Italy Serie A</p>
        <p><b>🏟 Match:</b> Juventus vs Genoa</p>
        <p><b>🎯 Total Goals (Over/Under 2.5):</b><br>Over: 40%<br>Under: 60%</p>
        <p><b>📘 BTTS:</b><br>Yes: 35%<br>No: 65%</p>
        <p><b>⏱️ Match Outcome:</b><br>Team 1 Win: 70%<br>Draw: 20%<br>Team 2 Win: 10%</p>
        <p><b>💡 Highest Probability Bet:</b><br><span style='color:blue;'>Juventus to win 70%</span></p>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/admin")
def admin():
    html = """
    <html>
    <head><title>Admin Panel</title></head>
    <body style='font-family:Arial; max-width:600px; margin:auto; padding:20px;'>
        <h2>Naksir Admin Panel</h2>
        <form action="/submit" method="post">
            Password:<br><input type="password" name="password" style="width:100%"><br><br>
            Competition:<br><input type="text" name="competition" style="width:100%"><br><br>
            Match:<br><input type="text" name="match" style="width:100%"><br><br>
            Highest Bet:<br><input type="text" name="highest" style="width:100%"><br><br>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/submit", methods=["POST"])
def submit():
    password = request.form.get("password")
    if password != "naksir2025":
        return "<h3 style='color:red;'>Wrong password</h3>"

    data = {
        "competition": request.form.get("competition"),
        "match": request.form.get("match"),
        "highestBet": request.form.get("highest")
    }
    with open("prediction.json", "w") as f:
        f.write(str(data))
    return "<h3 style='color:green;'>Submitted successfully</h3>"

@app.route("/webhook", methods=["POST"])
def webhook():
    return jsonify(ok=True)

@app.route("/create-invoice", methods=["POST"])
def create_invoice():
    return jsonify({
        "invoiceLink": "https://t.me/NaksirSoccerPredictions_bot?start=naksir_invoice"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
