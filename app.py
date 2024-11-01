from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# This is to temporarily replace user data database storage.
users_db = {}

# Signup endpoint
@app.route('/signup', methods=["POST"])
def signup():
    data = request.json

    # Get form data
    fullname: data.get("fullname")
    email = data.get("email")
    password = data.get("password")

    # Validate user input
    if not fullname or not email or not password:
        return jsonify({"error": "All fields are required."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    # Check if the user already exists
    if email in users_db:
        return jsonify({"error": "User already exists."}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    users_db[email] = {
        "fullname": fullname,
        "email": email,
        "password": password
    }

    return jsonify({"message": "You have successfully created an account!"}), 201

# Login endpoint
@app.route("/login", methods= ["POST"])
def login():
    data = request.json

    # Get form data
    email = data.get("email")
    password = data.get("password")

    # Validate user input
    if not email or not password:
        return jsonify({"error": "Email and password are required. Please fill in your details."}), 400

    # Find user
    user = users_db.get(email)
    if not user:
        return jsonify({"error": "User not found."}), 401

    # Check password
    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid password."}), 401

    return jsonify({"message": "Login successful."}), 200

if __name__ == "__main__":
    app.run(debug=True)