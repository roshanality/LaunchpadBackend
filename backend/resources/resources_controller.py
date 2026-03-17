from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core_middleware import get_user_id_from_jwt
from . import resources_model

resources_bp = Blueprint('resources_bp', __name__)

@resources_bp.route('/resources', methods=['GET'])
def get_resources():
    try:
        return jsonify(resources_model.get_resources(request.args.get('category'), request.args.get('search'))), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resources_bp.route('/resources', methods=['POST'])
@jwt_required()
def create_resource():
    try:
        resource_id, msg, code = resources_model.create_resource(get_user_id_from_jwt(), request.get_json() or {})
        if not resource_id: return jsonify({'error': msg}), code
        return jsonify({'message': msg, 'id': resource_id}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resources_bp.route('/resources/<int:resource_id>', methods=['PUT'])
@jwt_required()
def update_resource(resource_id):
    try:
        success, msg, code = resources_model.update_resource(get_user_id_from_jwt(), resource_id, request.get_json() or {})
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@resources_bp.route('/resources/<int:resource_id>', methods=['DELETE'])
@jwt_required()
def delete_resource(resource_id):
    try:
        success, msg, code = resources_model.delete_resource(get_user_id_from_jwt(), resource_id)
        if not success: return jsonify({'error': msg}), code
        return jsonify({'message': msg}), code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
