from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import get_all_users

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    users = get_all_users()
    return jsonify(users)

@users_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def admin_list_users():
    from models.user import get_all_users, get_user_by_id
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    if user['role'].lower() != 'admin':
        return jsonify({'msg': 'Only admin can view all users'}), 403
    users = get_all_users()
    return jsonify(users)

@users_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def admin_update_user_role(user_id):
    from models.user import get_user_by_id
    from models.user import update_user_role  # You may need to implement this in models/user.py
    admin_id = get_jwt_identity()
    admin = get_user_by_id(admin_id)
    if user.get('role', '').lower() != 'admin':
        return jsonify({'msg': 'Only admin can update user roles'}), 403
    data = request.get_json()
    new_role = data.get('role')
    if new_role not in ['admin', 'developer', 'reporter']:
        return jsonify({'msg': 'Invalid role'}), 400
    update_user_role(user_id, new_role)
    return jsonify({'success': True, 'msg': 'User role updated'}) 

