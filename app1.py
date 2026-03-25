import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

#backend file path
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

@app.route("/api")
def api_data():
    """Read data.json and return it as a JSON list."""
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
