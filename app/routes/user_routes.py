from flask import Blueprint, request, jsonify
from app.services.user_service import register_user, login_user, update_user_profile

user_bp = Blueprint("user", __name__)

# Route pour l'inscription
@user_bp.route("/signup", methods=["POST"])
def register():
    data = request.get_json()
    message, status_code = register_user(data)
    return jsonify(message), status_code

# Route pour la connexion
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    message, status_code = login_user(data)
    return jsonify(message), status_code

# Route pour updater le profil utilisateur
@user_bp.route("/update/<user_id>", methods=["PUT"])
def update_profile(user_id):
    data = request.get_json()
    message, status_code = update_user_profile(user_id, data)
    return jsonify(message), status_code
