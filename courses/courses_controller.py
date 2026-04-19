from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required
from core_middleware import get_user_id_from_jwt
from werkzeug.utils import secure_filename
import os
import uuid
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

@courses_bp.route('/courses/<int:course_id>/enrollment-status', methods=['GET'])
@jwt_required(optional=True)
def get_enrollment_status(course_id):
    try:
        user_id = get_user_id_from_jwt()
        if not user_id:
            return jsonify({'status': None}), 200
            
        status = courses_model.get_enrollment_status(user_id, course_id)
        return jsonify({'status': status}), 200
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
        user_id = get_user_id_from_jwt()
        screenshot_filename = None
        
        if 'screenshot' in request.files:
            file = request.files['screenshot']
            if file.filename:
                ext = os.path.splitext(file.filename)[1].lower()
                if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                    return jsonify({'error': 'Invalid file type for screenshot'}), 400
                screenshot_filename = f"payment_{course_id}_{user_id}_{uuid.uuid4().hex}{ext}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], screenshot_filename)
                file.save(file_path)

        success, msg, code = courses_model.enroll_course(user_id, course_id, screenshot_filename)
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

@courses_bp.route('/admin/courses/enrollments/<int:enrollment_id>/status', methods=['POST'])
@jwt_required()
def update_enrollment_status(enrollment_id):
    try:
        data = request.get_json() or {}
        status = data.get('status')
        message = data.get('message', '')
        
        if status not in ['approved', 'rejected']:
            return jsonify({'error': 'Invalid status'}), 400
            
        success, msg, code = courses_model.update_enrollment_status(get_user_id_from_jwt(), enrollment_id, status, message)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/payment-screenshot/<path:filename>')
def get_payment_screenshot(filename):
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404
