from flask import Flask
from config import Config
from extensions import db
from routes.auth_routes import auth_bp
from routes.job_routes import jobs_bp
from routes.company_routes import companies_bp
from routes.application_routes import applications_bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(applications_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
