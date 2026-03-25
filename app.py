import json
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

app = Flask(__name__)

# ── MongoDB Atlas URI ──────────────────────────────────────────────────────────
# Replace with your actual Atlas connection string
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://flaskuser:StrongPassword123@cluster0.feqrdcf.mongodb.net/mydb?retryWrites=true&w=majority"
)

def get_db():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return client["mydb"]

# ── Path to data.json ──────────────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

# ── /api — read data.json and return as JSON list ──────────────────────────────
@app.route("/api")
def api_data():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

# ── / — show the form ──────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", error=None)

# ── /submit — handle form POST ─────────────────────────────────────────────────
@app.route("/submit", methods=["POST"])
def submit():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    # Basic validation
    if not name or not email or not message:
        return render_template("index.html", error="All fields are required.")

    # ── 1. Save to data.json ───────────────────────────────────────────────────
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        # Generate next ID automatically
        next_id = max((item.get("id", 0) for item in data), default=0) + 1

        new_entry = {
            "id":      next_id,
            "name":    name,
            "email":   email,
            "message": message
        }
        data.append(new_entry)

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        return render_template("index.html", error=f"Failed to write to data.json: {e}")

    # ── 2. Save to MongoDB Atlas ───────────────────────────────────────────────
    try:
        db = get_db()
        db.submissions.insert_one(new_entry.copy())

    except ConnectionFailure:
        return render_template("index.html",
            error="Saved to data.json but could not connect to MongoDB. Check your MONGO_URI.")
    except OperationFailure as e:
        return render_template("index.html",
            error=f"Saved to data.json but MongoDB error: {e}")
    except Exception as e:
        return render_template("index.html",
            error=f"Saved to data.json but unexpected MongoDB error: {e}")

    # ── 3. Both succeeded — redirect to success page ───────────────────────────
    return redirect(url_for("success"))

# ── /success ───────────────────────────────────────────────────────────────────
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
