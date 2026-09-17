from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db

companies_bp = Blueprint("companies", __name__)

def recruiter_required():
    return "user_id" in session and session.get("role") == "recruiter"

@companies_bp.route("/recruiter/dashboard")
def recruiter_dashboard():
    if not recruiter_required():
        return redirect(url_for("auth.login"))

    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies WHERE recruiter_id=%s", (session["user_id"],))
    company = cursor.fetchone()

    jobs = []
    applicants = []
    if company:
        cursor.execute("""
            SELECT * FROM jobs
            WHERE company_id=%s
            ORDER BY created_at DESC
        """, (company["id"],))
        jobs = cursor.fetchall()

        cursor.execute("""
            SELECT applications.id, applications.status, applications.applied_at,
                   jobs.title, users.full_name, users.email
            FROM applications
            JOIN jobs ON applications.job_id = jobs.id
            JOIN users ON applications.candidate_id = users.id
            WHERE jobs.company_id=%s
            ORDER BY applications.applied_at DESC
        """, (company["id"],))
        applicants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("recruiter_dashboard.html", company=company, jobs=jobs, applicants=applicants)

@companies_bp.route("/company/create", methods=["POST"])
def create_company():
    if not recruiter_required():
        return redirect(url_for("auth.login"))

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO companies (recruiter_id, name, description, location, website)
        VALUES (%s,%s,%s,%s,%s)
    """, (
        session["user_id"],
        request.form["name"],
        request.form["description"],
        request.form["location"],
        request.form["website"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Company created.", "success")
    return redirect(url_for("companies.recruiter_dashboard"))

@companies_bp.route("/jobs/create", methods=["POST"])
def create_job():
    if not recruiter_required():
        return redirect(url_for("auth.login"))

    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM companies WHERE recruiter_id=%s", (session["user_id"],))
    company = cursor.fetchone()

    if not company:
        cursor.close()
        conn.close()
        flash("Create your company profile first.", "error")
        return redirect(url_for("companies.recruiter_dashboard"))

    cursor.execute("""
        INSERT INTO jobs
        (company_id, title, description, location, job_type, experience, salary, skills)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        company["id"],
        request.form["title"],
        request.form["description"],
        request.form["location"],
        request.form["job_type"],
        request.form["experience"],
        request.form["salary"],
        request.form["skills"]
    ))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Job posted successfully.", "success")
    return redirect(url_for("companies.recruiter_dashboard"))

@companies_bp.route("/jobs/delete/<int:job_id>", methods=["POST"])
def delete_job(job_id):
    if not recruiter_required():
        return redirect(url_for("auth.login"))

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE jobs FROM jobs
        JOIN companies ON jobs.company_id=companies.id
        WHERE jobs.id=%s AND companies.recruiter_id=%s
    """, (job_id, session["user_id"]))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Job deleted.", "success")
    return redirect(url_for("companies.recruiter_dashboard"))
