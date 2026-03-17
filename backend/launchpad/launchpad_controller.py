from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core_middleware import get_user_id_from_jwt
from . import launchpad_model

launchpad_bp = Blueprint('launchpad_bp', __name__)

@launchpad_bp.route('/launchpad/services', methods=['GET'])
def get_services():
    try:
        return jsonify(launchpad_model.get_services(request.args.get('category'), request.args.get('search'))), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/services/<int:service_id>', methods=['GET'])
def get_service_detail(service_id):
    try:
        service = launchpad_model.get_service_detail(service_id)
        if not service: return jsonify({'error': 'Service not found'}), 404
        return jsonify(service), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/services/<int:service_id>/timeline', methods=['GET'])
def get_service_timeline(service_id):
    try:
        return jsonify(launchpad_model.get_service_timeline(service_id)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/services', methods=['POST'])
@jwt_required()
def create_service():
    user_id = get_user_id_from_jwt()
    data = request.get_json()
    if not data or not all(k in data for k in ('title', 'description', 'category')):
        return jsonify({'error': 'title, description, category are required'}), 400
    try:
        service_id = launchpad_model.create_service(user_id, data)
        return jsonify({'message': 'Service created', 'id': service_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/my-services', methods=['GET'])
@jwt_required()
def get_my_services():
    try:
        return jsonify(launchpad_model.get_my_services(get_user_id_from_jwt())), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/services/<int:service_id>', methods=['PUT'])
@jwt_required()
def update_service(service_id):
    data = request.get_json() or {}
    try:
        success, msg, code = launchpad_model.update_service(get_user_id_from_jwt(), service_id, data)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/services/<int:service_id>', methods=['DELETE'])
@jwt_required()
def delete_service(service_id):
    try:
        success, msg, code = launchpad_model.delete_service(get_user_id_from_jwt(), service_id)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/requests', methods=['POST'])
@jwt_required()
def create_service_request():
    data = request.get_json()
    if not data or not all(k in data for k in ('project_type', 'description')):
        return jsonify({'error': 'project_type and description are required'}), 400
    try:
        req_id = launchpad_model.create_service_request(get_user_id_from_jwt(), data)
        return jsonify({'message': 'Request submitted', 'id': req_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/admin/requests', methods=['GET'])
@jwt_required()
def get_admin_service_requests():
    user_id = get_user_id_from_jwt()
    if not launchpad_model.is_admin(user_id): return jsonify({'error': 'Admin required'}), 403
    try:
        return jsonify(launchpad_model.get_admin_service_requests()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/admin/services/<int:service_id>/timeline', methods=['GET'])
@jwt_required()
def admin_get_timeline(service_id):
    if not launchpad_model.is_admin(get_user_id_from_jwt()): return jsonify({'error': 'Admin required'}), 403
    try:
        return jsonify(launchpad_model.get_service_timeline(service_id)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/admin/services/<int:service_id>/timeline', methods=['POST'])
@jwt_required()
def admin_create_timeline(service_id):
    if not launchpad_model.is_admin(get_user_id_from_jwt()): return jsonify({'error': 'Admin required'}), 403
    data = request.get_json() or {}
    if not data.get('title') or not data.get('description'): return jsonify({'error': 'title and description required'}), 400
    try:
        item_id = launchpad_model.admin_create_timeline_item(service_id, data)
        return jsonify({'message': 'Created', 'id': item_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/admin/timeline/<int:item_id>', methods=['PUT'])
@jwt_required()
def admin_update_timeline(iutem_id):
    if not launchpad_model.is_admin(get_user_id_from_jwt()): return jsonify({'error': 'Admin required'}), 403
    try:
        success, msg, code = launchpad_model.admin_update_timeline_item(item_id, request.get_json() or {})
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/admin/timeline/<int:item_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_timeline(item_id):
    if not launchpad_model.is_admin(get_user_id_from_jwt()): return jsonify({'error': 'Admin required'}), 403
    try:
        launchpad_model.admin_delete_timeline_item(item_id)
        return jsonify({'message': 'Deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/my-requests', methods=['GET'])
@jwt_required()
def get_my_requests():
    try:
        return jsonify(launchpad_model.get_my_service_requests(get_user_id_from_jwt())), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def require_student():
    user_id = get_user_id_from_jwt()
    if not launchpad_model.is_student(user_id):
        return None, (jsonify({'error': 'Student required'}), 403)
    return user_id, None

@launchpad_bp.route('/launchpad/student-profile', methods=['GET'])
@jwt_required()
def get_student_profile():
    user_id, err = require_student()
    if err: return err
    try:
        return jsonify(launchpad_model.get_student_service_profile(user_id)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/student-profile', methods=['POST'])
@jwt_required()
def upsert_student_profile():
    user_id, err = require_student()
    if err: return err
    try:
        launchpad_model.upsert_student_service_profile(user_id, request.get_json() or {})
        return jsonify({'message': 'Profile saved'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/my-allotments', methods=['GET'])
@jwt_required()
def get_my_allotments():
    user_id, err = require_student()
    if err: return err
    try:
        return jsonify(launchpad_model.get_my_allotments(user_id)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/allotments', methods=['POST'])
@jwt_required()
def create_allotment():
    if not launchpad_model.is_admin(get_user_id_from_jwt()): return jsonify({'error': 'Admin required'}), 403
    data = request.get_json() or {}
    sid, stid = data.get('service_id'), data.get('student_id')
    if not sid or not stid: return jsonify({'error': 'service_id and student_id required'}), 400
    try:
        success, msg, code = launchpad_model.create_allotment(sid, stid)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchpad_bp.route('/launchpad/allotments/<int:allotment_id>/agree', methods=['POST'])
@jwt_required()
def agree_allotment(allotment_id):
    user_id, err = require_student()
    if err: return err
    try:
        success, msg, code = launchpad_model.agree_allotment(user_id, allotment_id)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
