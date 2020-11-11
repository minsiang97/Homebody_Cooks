from flask import Blueprint, jsonify, request
from models.user import User
from models.order_checkout import OrderCheckout
from models.subscription_recipe import Subscription_Recipe
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from helpers import s3, upload_to_s3
import datetime
from helpers import gateway

transactions_api_blueprint = Blueprint('transactions_api',
                             __name__,
                             template_folder='templates')

@transactions_api_blueprint.route('/client_token', methods=['GET'])
@jwt_required
def index():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    client_token = gateway.client_token.generate()
    return jsonify({"token" : client_token})


