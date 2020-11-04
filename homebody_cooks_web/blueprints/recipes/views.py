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
from helpers import s3, upload_to_s3

recipes_blueprint = Blueprint('recipes',
                            __name__,
                            template_folder='templates')


@recipes_blueprint.route('/<recipe_id>/edit', methods=["GET"])
def edit(recipe_id):
    recipe = Recipe.get_or_none(Recipe.id == recipe_id)
    return render_template('recipes/edit.html', recipe_id = recipe.id)

@recipes_blueprint.route('/new/', methods=["POST"])
def create():
    recipe = Recipe(name=request.form.get("recipe_name"), description=request.form.get("recipe_description"))
    if recipe.save():
        flash("Recipe Name & Description Added")
        return redirect(url_for('ingredients.create'))
    else:
        flash("An error occured")
        return render_template('recipes/new.html')

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

@recipes_blueprint.route("/<recipe_id>/upload", methods=["POST"])
@login_required
def upload_image(recipe_id):
    recipe = Recipe.get_or_none(Recipe.id == recipe_id)

    if "recipe_image" not in request.files:
        return "No recipe_image key in request.files"

    file = request.files["recipe_image"]

    if file.filename == "":
        return "Please select a file"

    if file:
        file_path= upload_to_s3(file, "recipe")
        recipe.image_url = file_path
        if recipe.save():
            flash("Image Uploaded")
            return redirect(url_for("recipes.edit", recipe_id = recipe.id))
        else:
            flash("An error occured")
            return redirect(url_for("recipes.edit", recipe_id = recipe.id))
    else:
        flash("No file selected")
        return redirect(url_for("recipes.edit", recipe_id = recipe.id))
