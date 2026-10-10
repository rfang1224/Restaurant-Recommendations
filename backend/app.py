from flask import Flask, request, render_template_string
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "users.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

def initialize_database():
    with sqlite3.connect(DATABASE_PATH) as connection:
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)

@app.route("/api/signup", methods=["POST"])
def signup():
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not username or not email or not password:
        return "All fields are required.", 400

    if len(password) < 8:
        return "Password must be at least 8 characters.", 400

    password_hash = generate_password_hash(password)

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (username, email, password_hash)
            )

        return render_template_string("""
            <h1>Account created successfully!</h1>
            <p>Your account has been registered.</p>
            <a href="http://127.0.0.1:5500/signup.html">
                Return to sign up
            </a>
        """), 201

    except sqlite3.IntegrityError:
        return "Username or email is already registered.", 409


initialize_database()

if __name__ == "__main__":
    app.run(debug=True, port=5000)