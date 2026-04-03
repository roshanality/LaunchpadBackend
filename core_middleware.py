from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

def log_request_info():
    if request.method != 'OPTIONS':
        print(f"DEBUG: Incoming request: {request.method} {request.path}")
        print(f"DEBUG: Headers: {dict(request.headers)}")
        if request.method == 'POST':
            print(f"DEBUG: Body: {request.get_data(as_text=True)}")

def get_user_id_from_jwt():
    identity = get_jwt_identity()
    if identity and isinstance(identity, str) and identity.startswith('user_'):
        return int(identity.replace('user_', ''))
    return identity

def register_jwt_error_handlers(jwt):
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        print(f"DEBUG: Invalid token error: {error_string}")
        return jsonify({'error': f'Invalid token: {error_string}'}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"DEBUG: Expired token")
        return jsonify({'error': 'Token has expired'}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        print(f"DEBUG: Missing token error: {error_string}")
        return jsonify({'error': f'Missing token: {error_string}'}), 422
