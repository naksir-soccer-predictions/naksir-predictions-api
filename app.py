
from flask import Flask, request, render_template_string, redirect
import os
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)

TOKENS = {}

def generate_token(user_id):
    token = secrets.token_urlsafe(16)
    expiration = datetime.utcnow() + timedelta(minutes=60)
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
    """
    return render_template_string(html)

@app.route("/admin", methods=["GET"])
def admin():
    html = """
    <div style="padding: 30px; font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
      <h2>Admin Panel – Naksir Premium Predictions</h2>

      <label>Password:</label><br>
      <input type="password" id="pass" style="width:100%; padding:8px;"><br><br>

      <label>Competition:</label><br>
      <input type="text" id="competition" style="width:100%; padding:8px;"><br><br>

      <label>Match:</label><br>
      <input type="text" id="match" style="width:100%; padding:8px;"><br><br>

      <label>Over 2.5 Goals %:</label><br>
      <input type="text" id="over" style="width:100%; padding:8px;"><br><br>

      <label>Under 2.5 Goals %:</label><br>
      <input type="text" id="under" style="width:100%; padding:8px;"><br><br>

      <label>BTTS Yes %:</label><br>
      <input type="text" id="bttsYes" style="width:100%; padding:8px;"><br><br>

      <label>BTTS No %:</label><br>
      <input type="text" id="bttsNo" style="width:100%; padding:8px;"><br><br>

      <label>Match Outcome - Team 1 Win %:</label><br>
      <input type="text" id="win1" style="width:100%; padding:8px;"><br><br>

      <label>Draw %:</label><br>
      <input type="text" id="draw" style="width:100%; padding:8px;"><br><br>

      <label>Match Outcome - Team 2 Win %:</label><br>
      <input type="text" id="win2" style="width:100%; padding:8px;"><br><br>

      <label>Highest Probability Bet:</label><br>
      <input type="text" id="bestbet" style="width:100%; padding:8px;"><br><br>

      <button onclick="submitPrediction()" style="padding: 10px 30px;">Submit</button>

      <script>
        async function submitPrediction() {
          const password = document.getElementById("pass").value;
          if (password !== "naksir2024") {
            alert("Wrong password");
            return;
          }

          const data = {
            competition: document.getElementById("competition").value,
            match: document.getElementById("match").value,
            overUnder: {
              "Over 2.5 Goals": document.getElementById("over").value,
              "Under 2.5 Goals": document.getElementById("under").value
            },
            btts: {
              "Yes": document.getElementById("bttsYes").value,
              "No": document.getElementById("bttsNo").value
            },
            outcome: {
              "Team 1 Win": document.getElementById("win1").value,
              "Draw": document.getElementById("draw").value,
              "Team 2 Win": document.getElementById("win2").value
            },
            highestBet: document.getElementById("bestbet").value
          };

          console.log("Submitted prediction:", data);
          alert("Prediction submitted (simulated).");
        }
      </script>
    </div>
    """
    return render_template_string(html)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received webhook data:", data)
    return '', 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
