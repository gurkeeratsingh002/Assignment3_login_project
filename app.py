from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

# Input boundaries used for black-box Boundary Value Analysis.
MAX_EMAIL_LENGTH = 254
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 64

# Demo user data. Passwords are stored as hashes, not plain text.
USERS = {
    "student@example.com": {
        "name": "Student User",
        "password_hash": generate_password_hash("Password123"),
        "active": True,
    },
    "inactive@example.com": {
        "name": "Inactive User",
        "password_hash": generate_password_hash("Password123"),
        "active": False,
    },
}

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

LOGIN_PAGE = """
<!doctype html>
<html>
<head><title>Login Demo</title></head>
<body>
    <h2>Login Demo</h2>
    <form method="post" action="/login">
        <label>Email:</label>
        <input type="text" name="email" maxlength="254"><br><br>
        <label>Password:</label>
        <input type="password" name="password" minlength="8" maxlength="64"><br><br>
        <button type="submit">Login</button>
    </form>
    {% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>
"""


def validate_login_input(email: str, password: str):
    """Validate login input before checking credentials."""
    if not email:
        return False, "Email is required."
    if len(email) > MAX_EMAIL_LENGTH:
        return False, f"Email must not exceed {MAX_EMAIL_LENGTH} characters."
    if not EMAIL_PATTERN.fullmatch(email):
        return False, "Invalid email format."

    if not password:
        return False, "Password is required."
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    if len(password) > MAX_PASSWORD_LENGTH:
        return False, f"Password must not exceed {MAX_PASSWORD_LENGTH} characters."

    return True, ""


def authenticate_user(email: str, password: str):
    """Authenticate a user using a hashed-password comparison."""
    user = USERS.get(email)

    # Use one generic message so valid accounts are not revealed.
    if not user or not user["active"]:
        return False, "Invalid email or password."
    if not check_password_hash(user["password_hash"], password):
        return False, "Invalid email or password."

    return True, "Login successful."


@app.route("/", methods=["GET"])
def home():
    return render_template_string(LOGIN_PAGE, message="")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    valid, validation_message = validate_login_input(email, password)
    if not valid:
        return render_template_string(LOGIN_PAGE, message=validation_message), 400

    authenticated, login_message = authenticate_user(email, password)
    status_code = 200 if authenticated else 401
    return render_template_string(LOGIN_PAGE, message=login_message), status_code


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    valid, validation_message = validate_login_input(email, password)
    if not valid:
        return jsonify({"success": False, "message": validation_message}), 400

    authenticated, login_message = authenticate_user(email, password)
    if authenticated:
        return jsonify({"success": True, "message": login_message, "token": "demo-token-123"}), 200

    return jsonify({"success": False, "message": login_message}), 401


if __name__ == "__main__":
    app.run(debug=True)
# Minor update after black-box testing review
