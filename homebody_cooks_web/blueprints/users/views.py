from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user
from models.user import User
from models.subscription import Subscription
from models.subscription_recipe import Subscription_Recipe
from models.recipe import Recipe
from helpers import s3, upload_to_s3
from flask_mail import Message
from app import mail, send_message_create_user, send_msg_checkout
from datetime import date, timedelta

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
        send_message_create_user.delay(email = current_user.email, name = current_user.name)
        return redirect(url_for("subscriptions.show"))
    else:
        flash(f"{user.errors[0]}")
        return redirect(url_for("users.new"))

@users_blueprint.route("/<user_id>/view_cart", methods=["GET"])
@login_required
def view_cart(user_id):
    user = User.get_or_none(User.id == user_id)
    subscription_recipes = Subscription_Recipe.select().where(Subscription_Recipe.user == current_user.id, Subscription_Recipe.created_at >= datetime.date.today())
    return render_template("users/checkout.html", subscription_recipes = subscription_recipes, user = current_user)

@users_blueprint.route("/<user_id>/view_cart/<recipe_id>/delete", methods=["POST"])
@login_required
def delete_from_cart(user_id, recipe_id):
    user = User.get_or_none(User.id == user_id)
    recipe = Recipe.get_or_none(Recipe.id == recipe_id)
    if current_user.delete_from_cart(recipe):
        return redirect(url_for('users.view_cart', user_id = current_user.id))
    else :
        return redirect(url_for('users.view_cart', user_id = current_user.id))

@users_blueprint.route("/<user_id>/checkout", methods=['POST'])
@login_required
def checkout(user_id):
    user = User.get_or_none(User.id == user_id)
    subscription_recipes = Subscription_Recipe.select().where(Subscription_Recipe.user == current_user.id)
    if subscription_recipes:
        send_msg_checkout.delay(email=current_user.email, name=current_user.name)
        flash("Successfully ordered", "success")
        return redirect(url_for('home'))
    else:
        flash("Error occured during confirmation. Try again", "danger")
        return redirect(url_for('users.view_cart', user_id = current_user.id))

@users_blueprint.route('/<id>', methods=["GET"])
def show(id):
   user = User.get_or_none(User.id == id)
   return render_template("users/show.html", user = user)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    if user:
        if current_user.id == user.id:
            return render_template('users/edit.html', user=user)
        else:
            flash("You're not authorised.")
            return redirect(url_for('users.show'))
    else:
        return "User does not exist."

@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_by_id(id)
    if user:
        data = request.form
        hashed_password = user.password_hash
        result = check_password_hash(hashed_password, data.get('old_password'))
        if result:
            user.name = data.get('user_name')
            user.email = data.get('email')

            if data.get('password') !="":
                user.password = data.get('password')

            if user.save():
                return redirect(url_for("users.show", id = user.id))
            else:
                print(user.errors)
                return redirect(url_for("users.edit",id=current_user.id))
        else:
            flash("Wrong Confirmation Password")
            return redirect(url_for('users.edit', id=current_user.id))
    
    if user.save():
        flash("Update Successful")
        return redirect(url_for('users.show',username = current_user.username))
    else:
        flash("Update Not Successful")
        return redirect(url_for('users.edit', id = current_user.id))

@users_blueprint.route("/<id>/upload", methods=["POST"])
@login_required
def upload_profile(id):
    user = User.get_or_none(User.id == id)

    if "profile_image" not in request.files:
        return "No profile_image key in request.files"

    file = request.files["profile_image"]

    if file.filename == "":
        return "Please select a file"

    if file:
        file_path= upload_to_s3(file, "users")
        user.profile_image_url = file_path
        if user.save():
            flash("Image Uploaded")
            return redirect(url_for("users.show", id = user.id))
        else:
            flash("An error occured")
            return redirect(url_for("users.edit", id = user.id))
    else:
        flash("No file selected")
        return redirect(url_for("users.edit", id = user.id))

def reminder_friday():
    user_recipes = Subscription_Recipe.select().where(Subscription_Recipe.created_at.between(date.today() - timedelta(days = 5), date.today()))
    user_id = [u.user.id for u in user_recipes]
    to_send_email_id = User.select().where(User.id.not_in(user_id))
    to_send_email_list_friday = [u.email for u in to_send_email_id]

    return to_send_email_list_friday

def reminder_sunday():
    user_recipes = Subscription_Recipe.select().where(Subscription_Recipe.created_at.between(date.today() - timedelta(days = 7), date.today()))
    user_id = [u.user.id for u in user_recipes]
    to_send_email_id = User.select().where(User.id.not_in(user_id))
    to_send_email_list_sunday = [u.email for u in to_send_email_id]

    return to_send_email_list_sunday