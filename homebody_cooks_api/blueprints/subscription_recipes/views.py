from flask import Blueprint, jsonify, request
from models.subscription_recipe import Subscription_Recipe
from models.user import User
from models.recipe import Recipe
from models.order import Order
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app
import datetime
from peewee import fn
from datetime import date, timedelta



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
    subscription_recipes = Subscription_Recipe.select().where(Subscription_Recipe.user == user.id, Subscription_Recipe.created_at >= datetime.date.today(), Subscription_Recipe.is_checkedout == 0)
    return jsonify([{"id" : s.id, "user" : s.user.id, "subscription" : s.subscription.id, "recipe" : s.recipe.id, "recipe_image_path" : app.config.get("S3_LOCATION") + s.recipe.image_url, "recipe_name" : s.recipe.recipe_name}for s in subscription_recipes])

@subscription_recipes_api_blueprint.route('/me/week', methods=['GET'])
@jwt_required
def week():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    subscription_recipes = Subscription_Recipe.select().where(Subscription_Recipe.user == user.id, Subscription_Recipe.created_at.between(fn.date_trunc('week', date.today()), date.today() + timedelta(days=1)))
    return jsonify([{"id" : s.id, "user" : s.user.id, "subscription" : s.subscription.id, "recipe" : s.recipe.id, "recipe_image_path" : app.config.get("S3_LOCATION") + s.recipe.image_url, "recipe_name" : s.recipe.recipe_name}for s in subscription_recipes])

    


@subscription_recipes_api_blueprint.route('/me/<recipe_id>', methods=['POST'])
@jwt_required
def user_add_cart(recipe_id):
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    ingredients = request.json
    recipe = Recipe.get_or_none(Recipe.id == recipe_id)
    subscription_recipes = Subscription_Recipe.select().where(Subscription_Recipe.user == user.id, Subscription_Recipe.created_at.between(fn.date_trunc('week', date.today()), date.today() + timedelta(days=1)))
    temp = Subscription_Recipe.select().where(Subscription_Recipe.user == user.id, Subscription_Recipe.created_at >= datetime.date.today(), Subscription_Recipe.is_checkedout == 0, Subscription_Recipe.recipe == recipe.id )
    if temp :
        return jsonify({"message" : "Item is already in the cart"})
    else :
        if len(subscription_recipes) >= (user.subscription.amount_of_meals) :
            return jsonify({"message" : "You have reached the maximum amount of meals selected in a week"})
        else:
            new_subscription_recipe = Subscription_Recipe(user = user.id, subscription = user.subscription.id, recipe = recipe.id)
            new_subscription_recipe.save()
            for ingredient in ingredients :
                user_recipe = Subscription_Recipe.select().where(Subscription_Recipe.recipe == recipe.id, Subscription_Recipe.user == user.id).order_by(Subscription_Recipe.created_at.desc()).get()
                order = Order(subscription_recipe = user_recipe.id, ingredient = ingredient)
                order.save()
            if order.save():
                return jsonify({"message" : "Successfully added to cart"})
            else :
                return jsonify({"message" : "Error occured"})

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
