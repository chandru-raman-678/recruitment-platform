import mysql.connector
from flask import current_app

class MySQL:
    def init_app(self, app):
        pass

    def get_connection(self):
        return mysql.connector.connect(
            host=current_app.config["MYSQL_HOST"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DATABASE"],
        )

db = MySQL()
