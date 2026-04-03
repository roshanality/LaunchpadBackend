from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core_middleware import get_user_id_from_jwt
from . import messages_model

messages_bp = Blueprint('messages_bp', __name__)

@messages_bp.route('/admin/support-messages', methods=['GET'])
@jwt_required()
def get_support_messages():
    try:
        msgs, err, code = messages_model.get_support_messages(get_user_id_from_jwt())
        if err: return jsonify({'error': err}), code
        return jsonify(msgs), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messages_bp.route('/support/message', methods=['POST'])
@jwt_required()
def send_support_message():
    content = request.get_json().get('content')
    if not content: return jsonify({'error': 'Message content is required'}), 400
    try:
        success, msg, code = messages_model.send_support_message(get_user_id_from_jwt(), content)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messages_bp.route('/messages/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    try:
        return jsonify(messages_model.get_conversations(get_user_id_from_jwt())), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messages_bp.route('/messages/conversations', methods=['POST'])
@jwt_required()
def create_conversation():
    other_id = request.get_json().get('other_user_id')
    if not other_id: return jsonify({'error': 'other_user_id is required'}), 400
    try:
        conv_id = messages_model.create_conversation(get_user_id_from_jwt(), other_id)
        return jsonify({'id': conv_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messages_bp.route('/messages/conversations/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_conversation(conversation_id):
    try:
        u, err, code = messages_model.get_conversation(get_user_id_from_jwt(), conversation_id)
        if err: return jsonify({'error': err}), code
        return jsonify({'other_user': u}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messages_bp.route('/messages/conversations/<int:conversation_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(conversation_id):
    try:
        msgs, err, code = messages_model.get_messages(get_user_id_from_jwt(), conversation_id)
        if err: return jsonify({'error': err}), code
        return jsonify(msgs), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messages_bp.route('/messages/conversations/<int:conversation_id>/messages', methods=['POST'])
@jwt_required()
def send_message(conversation_id):
    content = request.get_json().get('content')
    if not content: return jsonify({'error': 'Message content is required'}), 400
    try:
        m, err, code = messages_model.send_message(get_user_id_from_jwt(), conversation_id, content)
        if err: return jsonify({'error': err}), code
        return jsonify(m), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messages_bp.route('/messages/available-users', methods=['GET'])
@jwt_required()
def get_available_users():
    try:
        return jsonify(messages_model.get_available_users(get_user_id_from_jwt())), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── Notifications ─────────────────────────────────────────────────────────────

@messages_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    try:
        notifs = messages_model.get_notifications(get_user_id_from_jwt())
        return jsonify(notifs), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messages_bp.route('/notifications', methods=['POST'])
@jwt_required()
def create_notification():
    data = request.get_json()
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'message is required'}), 400
    try:
        notif = messages_model.create_notification(get_user_id_from_jwt(), message, data.get('type', 'info'))
        return jsonify(notif), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messages_bp.route('/notifications/<int:notif_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notif_id):
    try:
        messages_model.mark_notification_read(get_user_id_from_jwt(), notif_id)
        return jsonify({'message': 'Marked as read'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@messages_bp.route('/notifications/<int:notif_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notif_id):
    try:
        messages_model.delete_notification(get_user_id_from_jwt(), notif_id)
        return jsonify({'message': 'Notification deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
