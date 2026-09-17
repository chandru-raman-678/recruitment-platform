from flask import Blueprint, request, redirect, url_for, session, flash
from extensions import db

applications_bp = Blueprint("applications", __name__)

@applications_bp.route("/jobs/<int:job_id>/apply", methods=["POST"])
def apply(job_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("role") != "candidate":
        flash("Only candidates can apply for jobs.", "error")
        return redirect(url_for("jobs.job_details", job_id=job_id))

    conn = db.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO applications (job_id, candidate_id, cover_letter)
            VALUES (%s,%s,%s)
        """, (job_id, session["user_id"], request.form.get("cover_letter", "")))
        conn.commit()
        flash("Application submitted.", "success")
    except Exception:
        conn.rollback()
        flash("You may have already applied for this job.", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("jobs.job_details", job_id=job_id))

@applications_bp.route("/applications/<int:application_id>/status", methods=["POST"])
def update_status(application_id):
    if "user_id" not in session or session.get("role") != "recruiter":
        return redirect(url_for("auth.login"))

    status = request.form["status"]
    allowed = {"Applied", "Under Review", "Shortlisted", "Interview", "Selected", "Rejected"}
    if status not in allowed:
        flash("Invalid application status.", "error")
        return redirect(url_for("companies.recruiter_dashboard"))

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE applications a
        JOIN jobs j ON a.job_id=j.id
        JOIN companies c ON j.company_id=c.id
        SET a.status=%s
        WHERE a.id=%s AND c.recruiter_id=%s
    """, (status, application_id, session["user_id"]))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Application status updated.", "success")
    return redirect(url_for("companies.recruiter_dashboard"))
