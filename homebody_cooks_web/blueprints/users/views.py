from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user
from models.user import User
from models.subscription import Subscription

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
