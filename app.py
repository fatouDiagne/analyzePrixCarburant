from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


client = MongoClient("mongodb://localhost:27017/")
db = client["carburant_db"]
collection = db["stations"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/stations", methods=["GET"])
def get_stations():
    ville = request.args.get("ville", "").strip().title()
    stations = list(collection.find({"ville": ville}, {"_id": 0}))
    return jsonify(stations)

if __name__ == "__main__":
    app.run(debug=True)
