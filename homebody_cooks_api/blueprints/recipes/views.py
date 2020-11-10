from flask import Blueprint, jsonify
from models.recipe import Recipe
from app import app

recipes_api_blueprint = Blueprint('recipes_api',
                             __name__,
                             template_folder='templates')

@recipes_api_blueprint.route('/', methods=['GET'])
def index():
    recipes = Recipe.select()
    return jsonify([{"id" : r.id, "recipe_name" : r.recipe_name, "description" : r.description, "meal_type" : r.meal_type, "image_url" : app.config.get('S3_LOCATION') + r.image_url} for r in recipes])

@recipes_api_blueprint.route('/vegetarian', methods=['GET'])
def vegetarian() :
    recipes = Recipe.select().where(Recipe.meal_type == "Vegetarian")
    return jsonify([{"id" : r.id, "recipe_name" : r.recipe_name, "description" : r.description, "meal_type" : r.meal_type, "image_url" : app.config.get('S3_LOCATION') + r.image_url} for r in recipes])

@recipes_api_blueprint.route('/mix', methods=['GET'])
def mix() :
    recipes = Recipe.select().where(Recipe.meal_type == "Mix")
    return jsonify([{"id" : r.id, "recipe_name" : r.recipe_name, "description" : r.description, "meal_type" : r.meal_type, "image_url" : app.config.get('S3_LOCATION') + r.image_url} for r in recipes])

@recipes_api_blueprint.route('/images', methods=['GET'])
def images():
    recipes = Recipe.select()
    return jsonify([{"recipe_image_path" : app.config.get("S3_LOCATION") + r.image_url} for r in recipes])

@recipes_api_blueprint.route('/<recipe_id>', methods=['GET'])
def recipe(recipe_id):
    recipe = Recipe.get_or_none(Recipe.id == recipe_id)
    return jsonify([{"id" : recipe.id, "recipe_name" : recipe.recipe_name, "description" : recipe.description, "meal_type" : recipe.meal_type, "image_url" : app.config.get('S3_LOCATION') + recipe.image_url}])
