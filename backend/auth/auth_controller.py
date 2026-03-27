from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .auth_model import (
    get_user_by_email, create_user, get_user_by_id,
    set_reset_token, get_user_by_reset_token, update_password,
    generate_otp, save_admin_otp, verify_admin_otp
)
from extensions import limiter
from email_utils import send_admin_otp
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'email', 'password', 'role']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    # Validate role
    valid_roles = ['student', 'alumni', 'founder', 'mentor', 'investor']
    if data['role'] not in valid_roles:
        return jsonify({'error': f"Invalid role. Must be one of: {', '.join(valid_roles)}"}), 400

    # Validate alumni-specific fields
    if data['role'] == 'alumni':
        if not data.get('graduation_year') or not data.get('department'):
            return jsonify({'error': 'Graduation year and department are required for alumni'}), 400

    try:
        # Check if user already exists
        if get_user_by_email(data['email']):
            return jsonify({'error': 'User already exists'}), 400

        # Hash password (force pbkdf2 — scrypt requires OpenSSL support not always available)
        password_hash = generate_password_hash(data['password'], method='pbkdf2:sha256')

        # Set is_approved: False for non-students
        is_approved = True if data['role'] == 'student' else False

        user_data = {
            'name': data['name'],
            'email': data['email'],
            'password_hash': password_hash,
            'role': data['role'],
            'graduation_year': data.get('graduation_year'),
            'department': data.get('department'),
            'is_approved': is_approved
        }

        user = create_user(user_data)

        # Remove password hash from response
        user.pop('password_hash', None)
        user['is_approved'] = bool(user['is_approved'])

        # Roles requiring admin approval: no token issued until approved
        if not user['is_approved']:
            return jsonify({
                'message': 'Registration successful. Your account is pending admin approval.',
                'user': user
            }), 202

        # Create access token
        access_token = create_access_token(identity=f"user_{user['id']}")

        return jsonify({
            'token': access_token,
            'user': user
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        user = get_user_by_email(data['email'])

        if not user or not check_password_hash(user['password_hash'], data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Roles that require admin approval before login
        if user['role'] in ('mentor', 'investor', 'founder', 'alumni') and not user.get('is_approved'):
            return jsonify({'error': 'Your account is pending admin approval. You will be notified once approved.'}), 403

        # Admin login requires OTP verification
        if user['role'] == 'admin':
            otp = generate_otp()
            save_admin_otp(user['id'], otp)
            sent = send_admin_otp(otp)
            if not sent:
                return jsonify({'error': 'Failed to send OTP email. Check SMTP configuration.'}), 500
            return jsonify({
                'otp_required': True,
                'user_id': user['id'],
                'message': 'OTP sent to admin email. Please verify to continue.'
            }), 200

        # Non-admin — return token immediately
        access_token = create_access_token(identity=f"user_{user['id']}")
        user.pop('password_hash', None)
        user['is_approved'] = bool(user['is_approved'])

        return jsonify({
            'token': access_token,
            'user': user
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/admin/verify-otp', methods=['POST'])
@limiter.limit("10 per minute")
def admin_verify_otp():
    data = request.get_json()
    user_id = data.get('user_id')
    otp = str(data.get('otp', '')).strip()

    if not user_id or not otp:
        return jsonify({'error': 'user_id and otp are required'}), 400

    try:
        if not verify_admin_otp(user_id, otp):
            return jsonify({'error': 'Invalid or expired OTP'}), 401

        user = get_user_by_id(user_id)
        if not user or user['role'] != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403

        access_token = create_access_token(identity=f"user_{user['id']}")
        user.pop('password_hash', None)
        user['is_approved'] = bool(user['is_approved'])

        return jsonify({
            'token': access_token,
            'user': user
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    """Issue a new token for an authenticated user (sliding window refresh)."""
    identity = get_jwt_identity()
    new_token = create_access_token(identity=identity)
    return jsonify({'token': new_token}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email', '').strip()

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = get_user_by_email(email)
    if not user:
        # Return success anyway to avoid user enumeration
        return jsonify({'message': 'If that email exists, a reset link has been sent.'}), 200

    token = secrets.token_urlsafe(32)
    expires_at = (datetime.utcnow() + timedelta(hours=1)).isoformat()
    set_reset_token(user['id'], token, expires_at)

    # In production, send via email (SendGrid/AWS SES).
    # For now, return the token in the response so it's testable.
    reset_link = f"/reset-password?token={token}"
    return jsonify({
        'message': 'Password reset link generated.',
        'reset_link': reset_link   # Remove this line in production
    }), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token', '').strip()
    new_password = data.get('password', '').strip()

    if not token or not new_password:
        return jsonify({'error': 'Token and new password are required'}), 400

    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    user = get_user_by_reset_token(token)
    if not user:
        return jsonify({'error': 'Invalid or expired reset token'}), 400

    # Check expiry
    try:
        expires_at = datetime.fromisoformat(user['reset_token_expires'])
        if datetime.utcnow() > expires_at:
            return jsonify({'error': 'Reset token has expired'}), 400
    except Exception:
        return jsonify({'error': 'Invalid token'}), 400

    password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
    update_password(user['id'], password_hash)

    return jsonify({'message': 'Password updated successfully.'}), 200

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """
    Placeholder for email verification.
    In production integrate with SendGrid/AWS SES.
    """
    data = request.get_json()
    token = data.get('token', '').strip()

    if not token:
        return jsonify({'error': 'Verification token is required'}), 400

    # TODO: validate token against DB and mark user as email_verified
    return jsonify({'message': 'Email verification is not yet configured on this server.'}), 501
