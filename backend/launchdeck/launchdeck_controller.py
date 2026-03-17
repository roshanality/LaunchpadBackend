import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from core_middleware import get_user_id_from_jwt
from . import launchdeck_model

launchdeck_bp = Blueprint('launchdeck_bp', __name__)

# --- Student/Alumni Mentorship (General) ---
@launchdeck_bp.route('/mentorship/request', methods=['POST'])
@jwt_required()
def request_mentorship():
    success, msg, code = launchdeck_model.create_student_mentorship_request(
        get_user_id_from_jwt(), request.json.get('alumni_id'), request.json.get('message', '')
    )
    if not success: return jsonify({'error': msg}), code
    return jsonify({'message': msg}), code

@launchdeck_bp.route('/mentorship/requests', methods=['POST', 'GET'])
@jwt_required()
def handle_mentorship_requests():
    user_id = get_user_id_from_jwt()
    if request.method == 'POST':
        success, msg, code = launchdeck_model.create_student_mentorship_request(
            user_id, request.json.get('alumni_id'), request.json.get('message', '')
        )
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    else:
        reqs, err, code = launchdeck_model.get_student_mentorship_requests(user_id)
        if err: return jsonify({'error': err}), code
        return jsonify(reqs), code

@launchdeck_bp.route('/mentorship/<int:request_id>/<action>', methods=['POST'])
@jwt_required()
def process_mentorship_request(request_id, action):
    if action not in ['accept', 'decline']: return jsonify({'error': 'Invalid action'}), 400
    success, msg, code = launchdeck_model.handle_student_mentorship_request(get_user_id_from_jwt(), request_id, action)
    if not success: return jsonify({'error': msg}), code
    return jsonify({'message': msg}), code

# --- Pitch Management ---
@launchdeck_bp.route('/launchdeck/upload/pitch-image', methods=['POST'])
@jwt_required()
def upload_pitch_image():
    if 'file' not in request.files: return jsonify({'error': 'No file'}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({'error': 'No file'}), 400
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if ext not in {'png', 'jpg', 'jpeg', 'gif', 'webp'}: return jsonify({'error': 'Invalid file type'}), 400
    filename = f"pitch_{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'filename': filename}), 200

@launchdeck_bp.route('/launchdeck/pitches', methods=['GET'])
def get_pitches():
    try:
        return jsonify(launchdeck_model.get_pitches(request.args.get('status', 'published'), request.args.get('category'), request.args.get('search'))), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/launchdeck/pitches/<int:pitch_id>', methods=['GET'])
def get_pitch_detail(pitch_id):
    try:
        pitch = launchdeck_model.get_pitch_detail(pitch_id)
        if not pitch: return jsonify({'error': 'Pitch not found'}), 404
        return jsonify(pitch), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/launchdeck/pitches', methods=['POST'])
@jwt_required()
def create_pitch():
    try:
        pitch_id, msg, code = launchdeck_model.create_pitch(get_user_id_from_jwt(), request.json)
        if not pitch_id: return jsonify({'error': msg}), code
        return jsonify({'message': msg, 'id': pitch_id}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/launchdeck/pitches/<int:pitch_id>', methods=['PUT'])
@jwt_required()
def update_pitch(pitch_id):
    try:
        success, msg, code = launchdeck_model.update_pitch(get_user_id_from_jwt(), pitch_id, request.json)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/launchdeck/pitches/<int:pitch_id>', methods=['DELETE'])
@jwt_required()
def delete_pitch(pitch_id):
    try:
        success, msg, code = launchdeck_model.delete_pitch(get_user_id_from_jwt(), pitch_id)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/launchdeck/my-pitches', methods=['GET'])
@jwt_required()
def get_my_pitches():
    try:
        return jsonify(launchdeck_model.get_my_pitches(get_user_id_from_jwt())), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Pitch Interests (Investors) ---
@launchdeck_bp.route('/launchdeck/pitches/<int:pitch_id>/interest', methods=['POST'])
@jwt_required()
def submit_interest(pitch_id):
    try:
        success, msg, code = launchdeck_model.submit_interest(get_user_id_from_jwt(), pitch_id, request.json.get('message', ''))
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/launchdeck/pitches/<int:pitch_id>/interest/check', methods=['GET'])
@jwt_required()
def check_interest(pitch_id):
    try:
        return jsonify(launchdeck_model.check_interest(get_user_id_from_jwt(), pitch_id)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Launchdeck Mentorship ---
@launchdeck_bp.route('/launchdeck/mentorship/request', methods=['POST'])
@jwt_required()
def launchdeck_request_mentorship():
    try:
        success, msg, code = launchdeck_model.launchdeck_request_mentorship(get_user_id_from_jwt(), request.json.get('pitch_id'), request.json.get('message', ''))
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/launchdeck/mentorship/requests', methods=['GET'])
@jwt_required()
def launchdeck_get_mentorship_requests():
    try:
        reqs, err, code = launchdeck_model.get_launchdeck_mentorship_requests(get_user_id_from_jwt())
        if err: return jsonify({'error': err}), code
        return jsonify(reqs), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/launchdeck/mentorship/requests/<int:request_id>', methods=['PUT'])
@jwt_required()
def launchdeck_update_mentorship_request(request_id):
    st = request.json.get('status')
    if st not in ('accepted', 'declined'): return jsonify({'error': 'Invalid status'}), 400
    try:
        success, msg, code = launchdeck_model.update_launchdeck_mentorship_request(get_user_id_from_jwt(), request_id, st)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Launchdeck Admin functions ---
@launchdeck_bp.route('/launchdeck/admin/notifications', methods=['GET'])
@jwt_required()
def get_launchdeck_notifications():
    try:
        nots, err, code = launchdeck_model.get_admin_notifications(get_user_id_from_jwt())
        if err: return jsonify({'error': err}), code
        return jsonify(nots), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/launchdeck/admin/notifications/<int:notif_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notif_id):
    try:
        success, msg, code = launchdeck_model.mark_admin_notification_read(get_user_id_from_jwt(), notif_id)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/admin/mentorship/assign', methods=['POST'])
@jwt_required()
def assign_mentor():
    data = request.json
    try:
        success, msg, code = launchdeck_model.assign_mentor(get_user_id_from_jwt(), data.get('request_id'), data.get('mentor_id'))
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/admin/mentors', methods=['GET'])
@jwt_required()
def get_launchdeck_mentors():
    try:
        mentors, err, code = launchdeck_model.get_launchdeck_mentors(get_user_id_from_jwt())
        if err: return jsonify({'error': err}), code
        return jsonify(mentors), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/admin/interests', methods=['GET'])
@jwt_required()
def get_all_interests():
    try:
        ints, err, code = launchdeck_model.get_all_interests(get_user_id_from_jwt())
        if err: return jsonify({'error': err}), code
        return jsonify(ints), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@launchdeck_bp.route('/admin/interests/<int:interest_id>/status', methods=['PUT'])
@jwt_required()
def update_interest_status(interest_id):
    try:
        success, msg, code = launchdeck_model.update_interest_status(get_user_id_from_jwt(), interest_id, request.json.get('status'))
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
