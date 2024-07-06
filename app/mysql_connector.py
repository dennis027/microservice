from flask_sqlalchemy import SQLAlchemy

mysql_db = SQLAlchemy()

def init_mysql_app(app):
    app.config['SQLALCHEMY_BINDS'] = {
        'mysql': f"mysql+pymysql://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}@{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}"
    }
    mysql_db.init_app(app)