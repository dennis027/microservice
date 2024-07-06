from flask import Blueprint, jsonify
from .mysql_connector import mysql_db

main_bp = Blueprint('main', __name__)

@main_bp.route('/mysql', methods=['GET'])
def get_mysql_data():
    result = mysql_db.session.execute("SELECT * FROM your_table").fetchall()
    return jsonify([dict(row) for row in result])
