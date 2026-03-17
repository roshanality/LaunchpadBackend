from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core_middleware import get_user_id_from_jwt
from . import courses_model

courses_bp = Blueprint('courses_bp', __name__)

@courses_bp.route('/courses', methods=['GET'])
def get_courses():
    try:
        return jsonify(courses_model.get_courses(request.args.get('search'), request.args.get('category'))), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_detail(course_id):
    try:
        course = courses_model.get_course_detail(course_id)
        if not course: return jsonify({'error': 'Course not found'}), 404
        return jsonify(course), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    try:
        course_id, msg, code = courses_model.create_course(get_user_id_from_jwt(), request.get_json() or {})
        if not course_id: return jsonify({'error': msg}), code
        return jsonify({'message': msg, 'id': course_id}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    try:
        success, msg, code = courses_model.update_course(get_user_id_from_jwt(), course_id, request.get_json() or {})
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
@jwt_required()
def enroll_course(course_id):
    try:
        success, msg, code = courses_model.enroll_course(get_user_id_from_jwt(), course_id)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/admin/courses', methods=['GET'])
@jwt_required()
def get_admin_courses():
    try:
        courses, err, code = courses_model.get_admin_courses(get_user_id_from_jwt())
        if err: return jsonify({'error': err}), code
        return jsonify(courses), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/admin/courses/<int:course_id>/students', methods=['GET'])
@jwt_required()
def get_course_students(course_id):
    try:
        students, err, code = courses_model.get_course_students(get_user_id_from_jwt(), course_id)
        if err: return jsonify({'error': err}), code
        return jsonify(students), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/users/enrolled-courses', methods=['GET'])
@jwt_required()
def get_user_enrolled_courses():
    try:
        return jsonify(courses_model.get_user_enrolled_courses(get_user_id_from_jwt())), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
