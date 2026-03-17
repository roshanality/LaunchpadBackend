import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
from core_middleware import get_user_id_from_jwt
from .profile_model import (
    get_user_data, update_user_profile, update_user_avatar,
    get_user_cv, update_user_cv, clear_user_cv,
    update_student_verification_data, get_dashboard_stats
)

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_user_id_from_jwt()
    try:
        user = get_user_data(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/<int:target_user_id>', methods=['GET'])
@jwt_required()
def get_user_profile_by_id(target_user_id):
    try:
        user = get_user_data(target_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        user.pop('id_card_image', None)
        return jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_user_id_from_jwt()
    data = request.get_json()
    try:
        update_user_profile(user_id, data)
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/upload-picture', methods=['POST'])
@jwt_required()
def upload_profile_picture():
    user_id = get_user_id_from_jwt()
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)
    file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if file_extension not in ['jpg', 'jpeg', 'png', 'gif']:
        return jsonify({'error': 'Invalid file type. Only JPG, PNG, and GIF are allowed.'}), 400
    
    unique_filename = f"{user_id}_{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    try:
        update_user_avatar(user_id, unique_filename)
        return jsonify({
            'message': 'Profile picture uploaded successfully',
            'filename': unique_filename,
            'url': f'/api/profile/picture/{unique_filename}'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/picture/<filename>')
def get_profile_picture(filename):
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@profile_bp.route('/cv', methods=['POST'])
@jwt_required()
def upload_cv():
    user_id = get_user_id_from_jwt()
    if 'cv' not in request.files:
        return jsonify({'error': 'No CV file provided'}), 400
    
    file = request.files['cv']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        filename = f"cv_{user_id}_{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        old_cv = get_user_cv(user_id)
        update_user_cv(user_id, filename)
        
        if old_cv:
            old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], old_cv)
            if os.path.exists(old_filepath):
                os.remove(old_filepath)
        
        return jsonify({
            'message': 'CV uploaded successfully',
            'cv_url': f'/api/profile/cv/{filename}'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/cv/<filename>')
def serve_cv(filename):
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@profile_bp.route('/cv', methods=['DELETE'])
@jwt_required()
def delete_cv():
    user_id = get_user_id_from_jwt()
    try:
        cv_filename = get_user_cv(user_id)
        if cv_filename:
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], cv_filename)
            if os.path.exists(filepath):
                os.remove(filepath)
            clear_user_cv(user_id)
        return jsonify({'message': 'CV deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/verification', methods=['GET'])
@jwt_required()
def get_verification():
    user_id = get_user_id_from_jwt()
    try:
        user = get_user_data(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({
            'roll_number': user.get('roll_number'),
            'id_card_image': user.get('id_card_image')
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/verification', methods=['POST'])
@jwt_required()
def update_verification():
    user_id = get_user_id_from_jwt()
    try:
        roll_number = None
        id_card_filename = None

        if request.content_type and 'multipart/form-data' in request.content_type:
            roll_number = request.form.get('roll_number')
            if 'id_card' in request.files:
                file = request.files['id_card']
                if file.filename:
                    ext = os.path.splitext(file.filename)[1]
                    id_card_filename = f"idcard_{user_id}_{int(datetime.now().timestamp())}{ext}"
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], id_card_filename))
        else:
            data = request.get_json() or {}
            roll_number = data.get('roll_number')

        if not update_student_verification_data(user_id, roll_number, id_card_filename):
            return jsonify({'error': 'No data to update'}), 400

        return jsonify({'message': 'Verification data updated', 'id_card_image': id_card_filename}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@profile_bp.route('/dashboard-stats', methods=['GET'])
@jwt_required()
def get_user_dashboard_stats():
    user_id = get_user_id_from_jwt()
    try:
        user = get_user_data(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        stats = get_dashboard_stats(user_id, user.get('role', 'student'))
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
