
from flask import Flask, request, render_template_string, redirect
import os
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)

TOKENS = {}
PREDICTIONS = {}
ADMIN_PASSWORD = "naksir2024"

def generate_token(user_id):
    token = secrets.token_urlsafe(16)
    expiration = datetime.utcnow() + timedelta(minutes=30)
    TOKENS[token] = {"user_id": user_id, "expires": expiration}
    return token

def validate_token(token):
    token_data = TOKENS.get(token)
    if not token_data or datetime.utcnow() > token_data["expires"]:
        TOKENS.pop(token, None)
        return False
    return True

@app.route("/")
def home():
    return "Naksir Prediction API is live"

@app.route("/generate-token", methods=["GET"])
def generate_token_route():
    user_id = request.args.get("user_id", "anonymous")
    token = generate_token(user_id)
    return {"token": token}

@app.route("/validate-token", methods=["GET"])
def validate_token_route():
    token = request.args.get("token")
    return {"valid": validate_token(token)}

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password != ADMIN_PASSWORD:
            return "<h3 style='color:red;'>Unauthorized</h3>"

        prediction = {
            "date": request.form.get("date"),
            "competition": request.form.get("competition"),
            "match": request.form.get("match"),
            "over": request.form.get("over"),
            "under": request.form.get("under"),
            "btts_yes": request.form.get("btts_yes"),
            "btts_no": request.form.get("btts_no"),
            "win1": request.form.get("win1"),
            "draw": request.form.get("draw"),
            "win2": request.form.get("win2"),
            "highest": request.form.get("highest")
        }

        PREDICTIONS["latest"] = prediction
        return redirect("/admin")

    html_form = """
    <h2>Naksir Admin Panel</h2>
    <form method='POST'>
        Password: <input type='password' name='password'><br><br>
        Date: <input type='text' name='date'><br>
        Competition: <input type='text' name='competition'><br>
        Match: <input type='text' name='match'><br>
        Over 2.5 %: <input type='text' name='over'><br>
        Under 2.5 %: <input type='text' name='under'><br>
        BTTS Yes %: <input type='text' name='btts_yes'><br>
        BTTS No %: <input type='text' name='btts_no'><br>
        Team 1 Win %: <input type='text' name='win1'><br>
        Draw %: <input type='text' name='draw'><br>
        Team 2 Win %: <input type='text' name='win2'><br>
        Highest Probability Bet: <input type='text' name='highest'><br><br>
        <input type='submit' value='Post Prediction'>
    </form>
    """
    return render_template_string(html_form)

@app.route("/soccer")
def soccer():
    token = request.args.get("token")
    if not token or not validate_token(token):
        return "<h2 style='color:red;'>❌ Unauthorized. Please access via Telegram Mini App.</h2>", 401

    p = PREDICTIONS.get("latest", {})
    html = f"""
    <html>
    <head>
        <title>Naksir Premium Predictions</title>
        <meta http-equiv="refresh" content="180">
        <style>
            body {{ font-family: Arial; text-align: center; padding: 20px; }}
        </style>
    </head>
    <body>
        <h2>⚽️ Naksir Premium Predictions ({p.get('date', '')})</h2>
        <p><b>Competition:</b> {p.get('competition', '')}</p>
        <p><b>Match:</b> {p.get('match', '')}</p>
        <p><b>Total Goals (Over/Under 2.5):</b><br>Over: {p.get('over', '')}%<br>Under: {p.get('under', '')}%</p>
        <p><b>BTTS:</b><br>Yes: {p.get('btts_yes', '')}%<br>No: {p.get('btts_no', '')}%</p>
        <p><b>Match Outcome:</b><br>Team 1 Win: {p.get('win1', '')}%<br>Draw: {p.get('draw', '')}%<br>Team 2 Win: {p.get('win2', '')}%</p>
        <p><b>💡 Highest Probability Bet:</b><br><span style='color:blue;'>{p.get('highest', '')}</span></p>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
