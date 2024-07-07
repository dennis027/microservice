from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_credentials.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class DBCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    db_type = db.Column(db.String(50), nullable=False)
    db_name = db.Column(db.String(50), nullable=False)
    db_user = db.Column(db.String(50), nullable=False)
    db_password = db.Column(db.String(50), nullable=False)
    db_host = db.Column(db.String(50), nullable=False)
    db_port = db.Column(db.Integer, nullable=False)

def get_db_credentials(db_id):
    credentials = DBCredentials.query.get(db_id)
    if credentials:
        return {
            'db_type': credentials.db_type,
            'db_name': credentials.db_name,
            'db_user': credentials.db_user,
            'db_password': credentials.db_password,
            'db_host': credentials.db_host,
            'db_port': credentials.db_port,
        }
    else:
        return None
def create_db_engine(credentials):
    if credentials['db_type'] == 'sqlite':
        db_url = f"sqlite:///{credentials['db_name']}"
    elif credentials['db_type'] == 'mysql':
        db_url = f"mysql+pymysql://{credentials['db_user']}:{credentials['db_password']}@{credentials['db_host']}:{credentials['db_port']}/{credentials['db_name']}"
    else:
        db_url = f"{credentials['db_type']}://{credentials['db_user']}:{credentials['db_password']}@{credentials['db_host']}:{credentials['db_port']}/{credentials['db_name']}"
    return create_engine(db_url)

@app.route('/', methods=['GET'])
def index():
    credentials = DBCredentials.query.all()
    databases = [{'id': cred.id, 'db_name': cred.db_name} for cred in credentials]
    return render_template('index.html', databases=databases)

@app.route('/tables/<int:db_id>', methods=['GET'])
def list_tables(db_id):
    credentials = get_db_credentials(db_id)
    if not credentials:
        return jsonify({'error': 'Database not found'}), 404

    engine = create_db_engine(credentials)
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            tables = [row[0] for row in result]
    except OperationalError as e:
        return render_template('error.html')

    return render_template('tables.html', db_id=db_id, db_name=credentials['db_name'], tables=tables)


@app.route('/data/<int:db_id>/<table_name>', methods=['GET'])
def get_table_data(db_id, table_name):
    credentials = get_db_credentials(db_id)
    if not credentials:
        return jsonify({'error': 'Database not found'}), 404

    engine = create_db_engine(credentials)
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT * FROM {table_name}"))
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result]
    except OperationalError as e:
        return render_template('error.html')

    return render_template('data.html', table_name=table_name, columns=columns, data=data)


@app.route('/add_db', methods=['POST'])
def add_db():
    db_type = request.form['db_type']
    db_name = request.form['db_name']
    db_user = request.form['db_user']
    db_password = request.form['db_password']
    db_host = request.form['db_host']
    db_port = request.form['db_port']

    new_db = DBCredentials(
        db_type=db_type,
        db_name=db_name,
        db_user=db_user,
        db_password=db_password,
        db_host=db_host,
        db_port=db_port
    )

    db.session.add(new_db)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
