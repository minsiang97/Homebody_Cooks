from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from flask_login import login_required, current_user, login_user
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.measurement import Measurement
from models.recipe_ingredient import RecipeIngredient
from models.subscription import Subscription
from models.user import User
from models.recipe import Recipe
from models.subscription_recipe import Subscription_Recipe

recipes_blueprint = Blueprint('recipes',
                            __name__,
                            template_folder='templates')


@recipes_blueprint.route('/new', methods=["GET"])
def new():
    return render_template('recipes/new.html')

@recipes_blueprint.route('/new/', methods=["POST"])
def create()
    pass

@recipes_blueprint.route("/show", methods=["GET"])
def show():
    recipes = Recipe.select()
    return render_template('recipes/show.html', recipes = recipes)

@recipes_blueprint.route("/<recipe_id>", methods=["POST"])
@login_required
def add_to_cart(recipe_id):
    recipe = Recipe.get_or_none(Recipe.id == recipe_id)
    subscription_recipe = Subscription_Recipe(user = current_user.id, subscription = current_user.subscription, recipe=recipe.id)
    if subscription_recipe.save():
        return redirect(url_for('recipes.show'))
    else :
        flash ("Failed to add to cart", "danger")
        return redirect(url_for('recipes.show'))

