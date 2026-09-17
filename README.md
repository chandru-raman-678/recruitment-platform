# Recruitment Platform

A beginner-friendly full-stack recruitment platform built with:

- HTML
- CSS
- JavaScript
- Python
- Flask
- MySQL

## Features in this starter version

### Public
- Home page
- Job listing
- Job search by keyword and location
- Job details

### Authentication
- Candidate registration/login
- Recruiter registration/login
- Password hashing
- Session-based authentication

### Candidate
- Apply for a job
- Add a cover letter
- View application status

### Recruiter
- Create company
- Post jobs
- Delete jobs
- View applicants
- Update application status

## Setup

1. Install Python 3.
2. Install MySQL Server.
3. Create a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

4. Install packages:

```bash
pip install -r requirements.txt
```

5. Create the database:

```bash
mysql -u root -p < database/schema.sql
```

Or open `database/schema.sql` in MySQL Workbench and execute it.

6. Copy `.env.example` to `.env` and enter your MySQL password.

7. Start Flask:

```bash
python app.py
```

8. Open:

http://127.0.0.1:5000

## Important

This is a learning/project foundation. Before production deployment, add CSRF protection, stronger validation, rate limiting, secure production configuration, migrations, logging, tests, resume upload validation, and proper secret management.
