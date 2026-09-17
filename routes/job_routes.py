from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/jobs")
def jobs():
    keyword = request.args.get("keyword", "").strip()
    location = request.args.get("location", "").strip()

    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT jobs.*, companies.name AS company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.id
        WHERE 1=1
    """
    params = []

    if keyword:
        query += " AND (jobs.title LIKE %s OR jobs.skills LIKE %s OR companies.name LIKE %s)"
        value = f"%{keyword}%"
        params.extend([value, value, value])

    if location:
        query += " AND jobs.location LIKE %s"
        params.append(f"%{location}%")

    query += " ORDER BY jobs.created_at DESC"

    cursor.execute(query, params)
    job_list = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("jobs.html", jobs=job_list, keyword=keyword, location=location)

@jobs_bp.route("/jobs/<int:job_id>")
def job_details(job_id):
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT jobs.*, companies.name AS company_name,
               companies.description AS company_description,
               companies.location AS company_location,
               companies.website
        FROM jobs
        JOIN companies ON jobs.company_id = companies.id
        WHERE jobs.id=%s
    """, (job_id,))
    job = cursor.fetchone()
    cursor.close()
    conn.close()

    if not job:
        flash("Job not found.", "error")
        return redirect(url_for("jobs.jobs"))

    return render_template("job_details.html", job=job)

@jobs_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session["role"] == "recruiter":
        return redirect(url_for("companies.recruiter_dashboard"))

    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT applications.*, jobs.title, companies.name AS company_name
        FROM applications
        JOIN jobs ON applications.job_id = jobs.id
        JOIN companies ON jobs.company_id = companies.id
        WHERE applications.candidate_id=%s
        ORDER BY applications.applied_at DESC
    """, (session["user_id"],))
    applications = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("candidate_dashboard.html", applications=applications)
