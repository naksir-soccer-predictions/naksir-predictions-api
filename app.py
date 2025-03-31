from flask import Flask, request, render_template_string, redirect
import os
import secrets
from datetime import datetime, timedelta

app = Flask("name")
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
    password = request.args.get("pw")
    if password != ADMIN_PASSWORD:
        return "<h3 style='color:red;'>Access Denied</h3>", 401

    if request.method == "POST":
        data = {
            "date": datetime.now().strftime("%d %b %Y"),
            "competition": request.form["competition"],
            "match": request.form["match"],
            "over": request.form["over"],
            "under": request.form["under"],
            "btts_yes": request.form["btts_yes"],
            "btts_no": request.form["btts_no"],
            "win1": request.form["win1"],
            "draw": request.form["draw"],
            "win2": request.form["win2"],
            "highest": request.form["highest"],
        }
        PREDICTIONS["today"] = data
        return redirect("/admin?pw=" + password)

    form_html = """
    <h2>Naksir Admin Panel</h2>
    <form method="post">
        Competition: <input name="competition"><br>
        Match: <input name="match"><br>
        Over %: <input name="over"><br>
        Under %: <input name="under"><br>
        BTTS Yes %: <input name="btts_yes"><br>
        BTTS No %: <input name="btts_no"><br>
        Win Team 1 %: <input name="win1"><br>
        Draw %: <input name="draw"><br>
        Win Team 2 %: <input name="win2"><br>
        Highest Bet: <input name="highest"><br>
        <button type="submit">Save</button>
    </form>
    """
    return render_template_string(form_html)

@app.route("/soccer")
def soccer():
    token = request.args.get("token")
    if not token or not validate_token(token):
        return "<h2 style='color:red;'>❌ Unauthorized. Please access via Telegram Mini App.</h2>", 401

    p = PREDICTIONS.get("today")
    if not p:
        return "<h3>No predictions published today yet.</h3>"

    html = f"""
    <html><head><title>Naksir Predictions</title></head><body>
    <h2>⚽️ Naksir Premium Predictions ({p['date']})</h2>
    <p><b>Competition:</b> {p['competition']}</p>
    <p><b>Match:</b> {p['match']}</p>
    <p><b>Total Goals (Over/Under 2.5):</b><br>Over: {p['over']}%<br>Under: {p['under']}%</p>
    <p><b>BTTS:</b><br>Yes: {p['btts_yes']}%<br>No: {p['btts_no']}%</p>
    <p><b>Match Outcome:</b><br>Team 1 Win: {p['win1']}%<br>Draw: {p['draw']}%<br>Team 2 Win: {p['win2']}%</p>
    <p><b>💡 Highest Probability Bet:</b><br><span style='color:blue;'>{p['highest']}</span></p>
    </body></html>
    """
    return html

if __name__ == "main":
    port = int(os.environ.get("PORT", 5000))  # Render sam postavi PORT, ne moraš ništa ručno
    app.run(host="0.0.0.0", port=port)