from models.recipe import Recipe
from models.ingredient import Ingredient
from models.measurement import Measurement
from models.recipe_ingredient import RecipeIngredient
from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from flask_login import login_required, current_user, login_user

recipes_blueprint = Blueprint('recipes',
                            __name__,
                            template_folder='templates')

@recipes_blueprint.route('/new', methods=["GET"])
def new():
    return render_template('recipes/new.html')

@recipes_blueprint.route('/new/', methods=["POST"])
def create()
    pass


