from flask import Blueprint, render_template, redirect, request, url_for, flash
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from helpers import oauth


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    data = request.form
    email = data.get("user_email")
    user = User.get_or_none(User.email == email)
    password_to_check = data.get("user_password")

    if user :
        hashed_password = user.password_hash
        result = check_password_hash(hashed_password, password_to_check)
        if result :
            login_user(user)
            flash ("Login successfully", "success")
            return redirect(url_for('home'))
        else :
            flash("Incorrect password", "danger")
            return redirect(url_for('sessions.new'))
    
    else :
        flash("Email does not exist", "danger")
        return redirect(url_for('sessions.new'))

@sessions_blueprint.route("/logout")
def logout():
    logout_user()
    flash("Successfully Logged Out!", "success")
    return redirect(url_for('home'))


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash("Successfully log in", "success")
        return redirect(url_for('home'))
    else:
        flash("Failed to log in", "danger")
        return redirect(url_for('sessions.new'))