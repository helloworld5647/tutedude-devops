from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/submit', methods=['POST'])
def submit():
    data =request.json
    name = data.get("name")
    email = data.get("email")

    return jsonify({
        "message": f"Data submitted successfully! Name: {name}, Email: {email}"
    })

app.run(host="0.0.0.0", port=5000)
