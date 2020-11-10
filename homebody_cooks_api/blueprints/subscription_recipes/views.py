from flask import Blueprint, jsonify, request
from models.subscription_recipe import Subscription_Recipe
from models.user import User
from models.recipe import Recipe
from models.order import Order
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app
import datetime

subscription_recipes_api_blueprint = Blueprint('subscription_recipes_api',
                             __name__,
                             template_folder='templates')

@subscription_recipes_api_blueprint.route('/', methods=['GET'])
def index():
    subscription_recipes = Subscription_Recipe.select()
    return jsonify([{"id" : s.id, "user" : s.user.id, "subscription" : s.subscription.id, "recipe" : s.recipe.id}for s in subscription_recipes])

@subscription_recipes_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def user():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    subscription_recipes = Subscription_Recipe.select().where(Subscription_Recipe.user == user.id)
    return jsonify([{"id" : s.id, "user" : s.user.id, "subscription" : s.subscription.id, "recipe" : s.recipe.id}for s in subscription_recipes])

@subscription_recipes_api_blueprint.route('/me/today', methods=['GET'])
@jwt_required
def today():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    subscription_recipes = Subscription_Recipe.select().where(Subscription_Recipe.user == user.id, Subscription_Recipe.created_at >= datetime.date.today())
    return jsonify([{"id" : s.id, "user" : s.user.id, "subscription" : s.subscription.id, "recipe" : s.recipe.id}for s in subscription_recipes])


@subscription_recipes_api_blueprint.route('/me/<recipe_id>/delete', methods=['DELETE'])
@jwt_required
def user_delete_cart(recipe_id):
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    recipe = Recipe.get_or_none(Recipe.id == recipe_id)
    if user.delete_from_cart(recipe):
        return jsonify({"message" : "Successfully Deleted"})
    else :
        return jsonify({"message" : "Error occured"})
