from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user
from models.user import User
from models.subscription import Subscription
from models.subscription_recipe import Subscription_Recipe
from models.recipe import Recipe

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form.get("password")
    user = User(name=request.form.get("user_name"), email=request.form.get("email"), password=user_password)
    if user.save():
        session["user_id"] = user.id
        login_user(user)
        flash('Successfully Signed Up')
        return redirect(url_for("home"))
    else:
        flash(f"{user.errors[0]}")
        return redirect(url_for("users.new"))

@users_blueprint.route("/<user_id>/checkout", methods=["GET"])
@login_required
def view_cart(user_id):
    user = User.get_or_none(User.id == user_id)
    subscription_recipes = Subscription_Recipe.select().where(Subscription_Recipe.user == current_user.id)
    return render_template("users/checkout.html", subscription_recipes = subscription_recipes, user = current_user)

@users_blueprint.route("/<user_id>/checkout/<recipe_id>/delete", methods=["POST"])
@login_required
def delete_from_cart(user_id, recipe_id):
    user = User.get_or_none(User.id == user_id)
    recipe = Recipe.get_or_none(Recipe.id == recipe_id)
    if current_user.delete_from_cart(recipe):
        return redirect(url_for('users.view_cart', user_id = current_user.id))
    else :
        return redirect(url_for('users.view_cart', user_id = current_user.id))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
