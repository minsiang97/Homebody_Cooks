from flask import Blueprint, jsonify, request
from models.user import User
from models.order_checkout import OrderCheckout
from models.subscription import Subscription
from models.subscription_recipe import Subscription_Recipe
from models.transaction import Transaction
from flask_jwt_extended import jwt_required, get_jwt_identity
from braintree.successful_result import SuccessfulResult
from flask_mail import Message 
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, send_message_first_payment
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


@transactions_api_blueprint.route('/<subscription_id>/payment', methods=['POST'])
@jwt_required
def payment(subscription_id):
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    subscription = Subscription.get_or_none(Subscription.id == subscription_id)
    nonce_from_the_client = request.json["temp"]
    result = gateway.customer.create({
        "first_name": user.name,
        "email": user.email,
        "payment_method_nonce": nonce_from_the_client
    })

    if result.is_success :
        result_subscription = gateway.subscription.create({
            "id" : user.id,
            "payment_method_token": result.customer.payment_methods[0].token,
            "plan_id": subscription.id
        })

    if type(result_subscription) == SuccessfulResult:
        user.is_valid = True
        user.subscription_id = subscription.id
        user.save()
        new_transaction = Transaction(amount = subscription.price, subscription = subscription.id , user = user.id)

        if new_transaction.save() and user.save():
            
            send_message_first_payment.delay(email = user.email, name = user.name)
            return jsonify({"message" : "Payment has been processed successfully"})

    else :
        return jsonify({"message" : "Payment failed, try again"})        
