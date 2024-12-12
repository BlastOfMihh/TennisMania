from flask import json, request


from flask import jsonify, session, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import bcrypt

from flask_socketio import send, emit

from .user_types import UserTypes

def training_sessions_routes(bp, socketio, training_sessions_service):
    @bp.route("/training_sessions", methods=["POST"])
    @jwt_required()
    def add_training_session():
        invoker=get_jwt_identity()
        user_id = invoker["id"]
        training_data = request.get_json()["content"]
        training_sessions_service.training_session_add(user_id, training_data)
        return jsonify({"status": "success"})
    
    @bp.route("/training_sessions/<int:id>", methods=["DELETE"])
    @jwt_required()
    def remove_training_session(id):
        training_sessions_service.training_session_remove(id)
        return jsonify({"status": "success"})
    
    @bp.route("/training_sessions/<int:id>", methods=["GET"])
    @jwt_required()
    def get_training_session(id):
        training_session = training_sessions_service.training_session_get(id)
        return jsonify(training_session)
    
