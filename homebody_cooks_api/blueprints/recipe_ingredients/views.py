from flask import Blueprint, jsonify
from models.recipe_ingredient import RecipeIngredient

recipe_ingredients_api_blueprint = Blueprint('recipe_ingredients_api',
                             __name__,
                             template_folder='templates')

@recipe_ingredients_api_blueprint.route('/', methods=['GET'])
def index():
    recipe_ingredients = RecipeIngredient.select()
    return jsonify([{"id" : r.id, "recipe_id" : r.recipe_id.id, "ingredient_id" : r.ingredient_id.id, "measurement_id" : r.measurement_id.id, "amount" : r.amount} for r in recipe_ingredients])

@recipe_ingredients_api_blueprint.route('/<recipe_id>', methods=['GET'])
def recipe(recipe_id):
    recipe_ingredients=RecipeIngredient.select().where(RecipeIngredient.recipe_id == recipe_id)
    return jsonify([{"id" : r.id, "recipe_id" : r.recipe_id.id, "ingredient_id" : r.ingredient_id.id, "measurement_id" : r.measurement_id.id, "amount" : r.amount} for r in recipe_ingredients])