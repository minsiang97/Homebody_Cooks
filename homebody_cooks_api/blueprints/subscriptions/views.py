from flask import Blueprint, jsonify
from models.subscription import Subscription

subscriptions_api_blueprint = Blueprint('subscriptions_api',
                             __name__,
                             template_folder='templates')

@subscriptions_api_blueprint.route('/', methods=['GET'])
def index():
    subscriptions = Subscription.select()
    return jsonify([{"id" : s.id, "name" : s.name, "amount_of_meals" : s.amount_of_meals, "price" : s.price, "description" : s.description} for s in subscriptions])