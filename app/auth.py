from functools import wraps
from flask import request, jsonify, current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-tokens')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        # Verify the token (this is a simple example, use a more secure method in production)
        if token != current_app.config['SECRET_KEY']:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)
    return decorated