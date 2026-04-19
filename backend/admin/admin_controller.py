from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core_middleware import get_user_id_from_jwt
from . import admin_model
from profile.profile_model import get_user_data, get_dashboard_stats

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/students/verification', methods=['GET'])
@jwt_required()
def get_admin_student_verifications():
    try:
        data, err, code = admin_model.get_admin_student_verifications(get_user_id_from_jwt())
        if err: return jsonify({'error': err}), code
        return jsonify(data), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/pending-users', methods=['GET'])
@admin_bp.route('/pending-founders', methods=['GET']) # ALIAS FOR BACKWARDS COMPATIBILITY
@jwt_required()
def get_pending_users():
    try:
        users, err, code = admin_model.get_pending_users(get_user_id_from_jwt())
        if err: return jsonify({'error': err}), code
        return jsonify(users), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:target_id>/approve', methods=['POST'])
@admin_bp.route('/founders/<int:target_id>/approve', methods=['POST']) # ALIAS FOR BACKWARDS COMPATIBILITY
@jwt_required()
def approve_user(target_id):
    try:
        success, msg, code = admin_model.approve_user(get_user_id_from_jwt(), target_id)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:target_id>/reject', methods=['POST'])
@admin_bp.route('/founders/<int:target_id>/reject', methods=['POST']) # ALIAS FOR BACKWARDS COMPATIBILITY
@jwt_required()
def reject_user(target_id):
    try:
        success, msg, code = admin_model.reject_user(get_user_id_from_jwt(), target_id)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_admin_stats():
    try:
        stats, err, code = admin_model.get_admin_stats(get_user_id_from_jwt())
        if err: return jsonify({'error': err}), code
        return jsonify(stats), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/stats', methods=['POST'])
@jwt_required()
def update_admin_stat():
    try:
        stat, err, code = admin_model.update_admin_stat(get_user_id_from_jwt(), request.get_json() or {})
        if err: return jsonify({'error': err}), code
        return jsonify({'message': 'Stat updated successfully', 'stat': stat}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users_admin():
    try:
        users, err, code = admin_model.get_all_users_admin(get_user_id_from_jwt(), request.args.get('role'))
        if err: return jsonify({'error': err}), code
        return jsonify(users), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/alumni/dashboard-stats', methods=['GET'])
@jwt_required()
def alumni_dashboard_stats():
    """Alias for /api/profile/dashboard-stats — used by the alumni/founder/mentor/investor dashboard."""
    user_id = get_user_id_from_jwt()
    try:
        user = get_user_data(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        role = user.get('role', 'alumni')
        if role not in ('alumni', 'founder', 'mentor', 'investor'):
            return jsonify({'error': 'Only alumni can access dashboard stats'}), 403
        stats = get_dashboard_stats(user_id, role)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/block', methods=['POST'])
@jwt_required()
def toggle_block_user(user_id):
    should_block = (request.get_json() or {}).get('block', True)
    try:
        success, msg, code = admin_model.toggle_block_user(get_user_id_from_jwt(), user_id, should_block)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
