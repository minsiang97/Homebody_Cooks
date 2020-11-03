from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from flask_login import login_required, current_user, login_user
from models.ingredient import Ingredient

ingredients_blueprint = Blueprint('ingredients',
                            __name__,
                            template_folder='templates')

# @ingredients_blueprint.route('/new', methods=["GET"])
# def new():
#     return render_template('ingredients/new.html')

# @ingredients_blueprint.route('/new/', methods=["POST"])
# def create():
#     ingredients = Ingredient(name=request.form.get(""))
#     ingredients_list = {}
#     if ingredients.save():
#         flash("Ingredients Added")
#         return redirect(url_for('recipe_ingredients.create'))
#     else:
#         flash("An error occured")
#         return render_template('recipes/new.html')