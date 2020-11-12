from flask import Blueprint, jsonify
from models.subscription import Subscription
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from helpers import gateway

subscriptions_api_blueprint = Blueprint('subscriptions_api',
                             __name__,
                             template_folder='templates')

@subscriptions_api_blueprint.route('/', methods=['GET'])
def index():
    subscriptions = Subscription.select()
    return jsonify([{"id" : s.id, "name" : s.name, "amount_of_meals" : s.amount_of_meals, "price" : s.price, "description" : s.description} for s in subscriptions])

@subscriptions_api_blueprint.route('/<plan_id>/change_plan', methods=["POST"])
@jwt_required
def update(plan_id):
    subscription_plan = Subscription.get_by_id(plan_id)
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    result = gateway.subscription.update(str(user_id), {
        "price" : subscription_plan.price,
        "plan_id" : subscription_plan.id,
        })
    
    if result.is_success :
        user.subscription = subscription_plan
        
        if user.save():
            return jsonify({"message" : "Plan changed successfully!"})
        else :
            return jsonify({"message" : "Failed to change plan!"})
    
    else :
        return jsonify({"message" : "Failed to change plan!"})