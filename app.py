
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

JSON_FILE = "prediction.json"

@app.route("/")
def index():
    return "Naksir Prediction API is live"

@app.route("/get", methods=["GET"])
def get_prediction():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/update", methods=["POST"])
def update_prediction():
    data = request.get_json()
    password = request.args.get("pass")

    if password != "naksir2025":
        return jsonify({"error": "Unauthorized"}), 403

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return jsonify({"status": "Prediction updated successfully"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
