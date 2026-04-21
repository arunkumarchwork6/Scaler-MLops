from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Flask API for Streamlit Integration!"

@app.route('/api/data', methods=['GET'])
def get_data():
    # Simulate a backend process (e.g., database query)
    stats = {
        "accuracy": round(random.uniform(0.85, 0.99), 2),
        "status": "Online",
        "processed_items": random.randint(100, 1000)
    }
    return jsonify(stats)

if __name__ == '__main__':
    # Flask defaults to port 5000
    app.run(debug=True, port=5000)
