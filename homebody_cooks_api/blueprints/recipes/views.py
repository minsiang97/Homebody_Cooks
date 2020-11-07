from flask import Blueprint, jsonify
from models.recipe import Recipe
from flask_jwt_extended import jwt_required, get_jwt_identity

recipes_api_blueprint = Blueprint('recipes_api',
                             __name__,
                             template_folder='templates')

@recipes_api_blueprint.route('/', methods=['GET'])
def index():
    recipes = Recipe.select()
    return jsonify([{"id" : r.id, "recipe_name" : r.recipe_name, "description" : r.description, "meal_type" : r.meal_type, "image_url" : u.image_url} for r in recipes])

@recipes_api_blueprint.route('/vegetarian', methods=['GET'])
def vegetarian() :
    recipes = Recipe.select().where(Recipe.meal_type == "Vegetarian")
    return jsonify([{"id" : r.id, "recipe_name" : r.recipe_name, "description" : r.description, "meal_type" : r.meal_type, "image_url" : u.image_url} for r in recipes])

@recipes_api_blueprint.route('/mix', methods=['GET'])
def mix() :
    recipes = Recipe.select().where(Recipe.meal_type == "Mix")
    return jsonify([{"id" : r.id, "recipe_name" : r.recipe_name, "description" : r.description, "meal_type" : r.meal_type, "image_url" : u.image_url} for r in recipes])