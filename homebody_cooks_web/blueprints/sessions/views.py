from flask import Blueprint, render_template
from werkzeug.security import check_password_hash


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
            