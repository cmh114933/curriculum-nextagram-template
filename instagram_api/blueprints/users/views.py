from flask import Blueprint, jsonify
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()
    return jsonify([{"id": u.id, "email": u.email} for u in users])

@users_api_blueprint.route("/me", methods=["GET"])
@jwt_required
def me():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password_hash": user.password_hash,
            "is_private": user.is_private
        })