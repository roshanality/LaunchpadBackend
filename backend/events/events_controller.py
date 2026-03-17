import jwt
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from core_middleware import get_user_id_from_jwt
from . import events_model

events_bp = Blueprint('events_bp', __name__)

def get_optional_user_id():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            return payload['sub']
        except:
            pass
    return None

@events_bp.route('/users/enrolled-events', methods=['GET'])
@jwt_required()
def get_user_enrolled_events():
    try:
        return jsonify(events_model.get_user_enrolled_events(get_user_id_from_jwt())), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@events_bp.route('/events', methods=['GET'])
def get_events():
    try:
        return jsonify(events_model.get_events(get_optional_user_id())), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@events_bp.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    try:
        event = events_model.get_event(event_id, get_optional_user_id())
        if not event: return jsonify({'error': 'Event not found'}), 404
        return jsonify(event), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@events_bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    try:
        event_id, msg, code = events_model.create_event(get_user_id_from_jwt(), request.get_json() or {})
        if not event_id: return jsonify({'error': msg}), code
        return jsonify({'message': msg, 'id': event_id}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@events_bp.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    try:
        success, msg, code = events_model.update_event(get_user_id_from_jwt(), event_id, request.get_json() or {})
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@events_bp.route('/events/<int:event_id>/enroll', methods=['POST'])
@jwt_required()
def enroll_event(event_id):
    try:
        success, msg, code = events_model.enroll_event(get_user_id_from_jwt(), event_id)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@events_bp.route('/admin/events/<int:event_id>/attendees', methods=['GET'])
@jwt_required()
def get_event_attendees(event_id):
    try:
        attendees, err, code = events_model.get_event_attendees(get_user_id_from_jwt(), event_id)
        if err: return jsonify({'error': err}), code
        return jsonify(attendees), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@events_bp.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    try:
        success, msg, code = events_model.delete_event(get_user_id_from_jwt(), event_id)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
