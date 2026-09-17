from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT jobs.*, companies.name AS company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.id
        ORDER BY jobs.created_at DESC
        LIMIT 6
    """)
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", jobs=jobs)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        role = request.form["role"]

        if not full_name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("auth.register"))

        if role not in ("candidate", "recruiter"):
            flash("Invalid role.", "error")
            return redirect(url_for("auth.register"))

        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (full_name, email, password_hash, role) VALUES (%s,%s,%s,%s)",
                (full_name, email, generate_password_hash(password), role)
            )
            conn.commit()
            flash("Registration successful. Please login.", "success")
        except Exception:
            conn.rollback()
            flash("Email may already be registered.", "error")
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            session["role"] = user["role"]
            return redirect(url_for("jobs.dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.home"))
