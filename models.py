from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DBCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    db_type = db.Column(db.String(50), nullable=False)
    db_name = db.Column(db.String(50), nullable=False)
    db_user = db.Column(db.String(50), nullable=False)
    db_password = db.Column(db.String(50), nullable=False)
    db_host = db.Column(db.String(50), nullable=False)
    db_port = db.Column(db.Integer, nullable=False)
