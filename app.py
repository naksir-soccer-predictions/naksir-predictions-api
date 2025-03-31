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
    if not token_data:
        return False
    if datetime.utcnow() > token_data["expires"]:
        del TOKENS[token]
        return False
    return True

@app.route("/")
def home():
    return "Naksir Prediction API is live"

@app.route("/generate-token")
def generate_token_route():
    user_id = request.args.get("user_id", "anonymous")
    token = generate_token(user_id)
    return {"token": token}

@app.route("/validate-token")
def validate_token_route():
    token = request.args.get("token")
    return {"valid": validate_token(token)}

@app.route("/admin", methods=["GET", "POST"])
def admin():
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        return "Unauthorized", 401

    if request.method == "POST":
        PREDICTIONS["prediction"] = {
            "date": request.form["date"],
            "competition": request.form["competition"],
            "match": request.form["match"],
            "over": request.form["over"],
            "under": request.form["under"],
            "btts_yes": request.form["btts_yes"],
            "btts_no": request.form["btts_no"],
            "win1": request.form["win1"],
            "draw": request.form["draw"],
            "win2": request.form["win2"],
            "highest": request.form["highest"]
        }
        return redirect("/admin?password=" + password)

    form_html = """
    <form method="POST">
        <input name="date" placeholder="Date"><br>
        <input name="competition" placeholder="Competition"><br>
        <input name="match" placeholder="Match"><br>
        <input name="over" placeholder="Over 2.5 %"><br>
        <input name="under" placeholder="Under 2.5 %"><br>
        <input name="btts_yes" placeholder="BTTS Yes %"><br>
        <input name="btts_no" placeholder="BTTS No %"><br>
        <input name="win1" placeholder="Team 1 Win %"><br>
        <input name="draw" placeholder="Draw %"><br>
        <input name="win2" placeholder="Team 2 Win %"><br>
        <input name="highest" placeholder="Highest Bet"><br>
        <button type="submit">Submit</button>
    </form>
    """
    return render_template_string(form_html)

@app.route("/soccer")
def soccer():
    token = request.args.get("token")
    if not token or not validate_token(token):
        return "<h2 style='color:red;'>❌ Unauthorized. Please access via Telegram Mini App.</h2>", 401

    p = PREDICTIONS.get("prediction", {})
    if not p:
        return "<h2>No predictions available yet.</h2>"

    html = f"""
    <html><head><meta http-equiv='refresh' content='60'></head><body>
    <h2>⚽ Naksir Premium Predictions ({p['date']})</h2>
    <p><b>Competition:</b> {p['competition']}</p>
    <p><b>Match:</b> {p['match']}</p>
    <p><b>Total Goals (Over/Under 2.5):</b><br>Over: {p['over']}%<br>Under: {p['under']}%</p>
    <p><b>BTTS:</b><br>Yes: {p['btts_yes']}%<br>No: {p['btts_no']}%</p>
    <p><b>Match Outcome:</b><br>Team 1 Win: {p['win1']}%<br>Draw: {p['draw']}%<br>Team 2 Win: {p['win2']}%</p>
    <p><b>💡 Highest Probability Bet:</b><br><span style='color:blue;'>{p['highest']}</span></p>
    </body></html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
