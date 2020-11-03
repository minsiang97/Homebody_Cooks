from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from flask_login import login_required, current_user, login_user
from models.recipe_ingredient import RecipeIngredient

recipe_ingredients_blueprint = Blueprint('recipe_ingredients',
                            __name__,
                            template_folder='templates')