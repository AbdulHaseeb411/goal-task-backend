from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Allow frontend to connect

# MongoDB Connection
MONGO_URI = "mongodb+srv://haseeboffice411:haseeb415855@cluster0.nxtos.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["goal_task_db"]  # Database name
users_collection = db["users"]  # Collection name

# User Signup API
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")  # In a real app, hash the password!

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # Check if user already exists
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    # Save user to MongoDB
    users_collection.insert_one({"username": username, "password": password})
    return jsonify({"message": "User registered successfully"}), 201

# User Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username, "password": password})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

