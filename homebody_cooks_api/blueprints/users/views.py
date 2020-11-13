from flask import Blueprint, jsonify, request
from models.user import User
from models.order_checkout import OrderCheckout
from models.subscription_recipe import Subscription_Recipe
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, send_message_create_user, send_msg_checkout
from helpers import s3, upload_to_s3
import datetime

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()
    return jsonify([{"id" : u.id, "email" : u.email, "name" : u.name, "is_admin" : u.is_admin, "is_valid" : u.is_valid} for u in users])


@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def me():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    if user :
        if user.subscription :
            return jsonify({
                "id" : user.id, 
                "name" : user.name,
                "email" : user.email, 
                "password_hash" : user.password_hash,
                "is_admin" : user.is_admin, 
                "is_valid" : user.is_valid,
                "subscription_id" : user.subscription.id,
                "subscription_name" : user.subscription.name
            })
        else :
            return jsonify({
                "id" : user.id, 
                "name" : user.name,
                "email" : user.email, 
                "password_hash" : user.password_hash,
                "is_admin" : user.is_admin, 
                "is_valid" : user.is_valid,
                "subscription_id" : "undefined",
                "subscription_name" : "No Plan Selected"
            })

@users_api_blueprint.route('/me/update', methods=['PUT'])
@jwt_required
def update():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    if user:
        data = request.json
        hashed_password = user.password_hash
        result = check_password_hash(hashed_password, data.get('old_password'))
        if result:
            user.name = data.get('user_name')
            user.email = data.get('email')

            if data.get('password') !="":
                user.password = data.get('password')

            if user.save():
                return jsonify({"message" : "User updated successfully"})
            else:
                return jsonify({"message" : "Failed to update user information"})
        else:
            return jsonify({"message" : "Wrong Old Password"})
    
    else:
        return jsonify({"message" : "Failed to update user information"})
        


@users_api_blueprint.route('/', methods = ["POST"])
def create_user():
    data = request.json
    hashed_password = generate_password_hash(data.get("password"))
    new_user = User(name = data.get("user_name"), password_hash = hashed_password, email = data.get("email"))
    if new_user.save() :
        token = create_access_token(identity = new_user.id)
        send_message_create_user.delay(email = new_user.email, name = new_user.name)
        return jsonify({"message" : "New User Created!", "token" : token})
    else :
        return jsonify({"message" : "Error occured, try again"})

@users_api_blueprint.route('/images/me', methods=['GET'])
@jwt_required
def get_user_image():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    if user :
        return jsonify({
            "profile_image_path" : app.config.get("S3_LOCATION") + user.profile_image_url
        })


@users_api_blueprint.route('/images', methods=['POST'])
@jwt_required
def post_user_image():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)

    if "profile_image" not in request.files:
        return jsonify({"messages" : "No profile_image key in request.files"}) 

    file = request.files["profile_image"]

    if file.filename == "":
        return jsonify({"messages" : "Please select a file"})

    if file:
        file_path= upload_to_s3(file, "users")
        user.profile_image_url = file_path
        if user.save():
            return jsonify({"messages" : "Uploaded successfully", "profile_image_path" : app.config.get("S3_LOCATION") + user.profile_image_url})
        else:
            return jsonify({"messages" : "Error occured during uploading"})
    else:
        
        return jsonify({"messages" : "No file selected"})

@users_api_blueprint.route('/me/checkout', methods=['POST'])
@jwt_required
def checkout():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    subscription_recipes = Subscription_Recipe.select().where(Subscription_Recipe.user == user.id, Subscription_Recipe.created_at >= datetime.date.today(), Subscription_Recipe.is_checkedout == 0)
    for s in subscription_recipes :
        order_checkout = OrderCheckout(subscription_recipe = s.id, user = user.id)
        order_checkout.save()
        s.is_checkedout = 1
        s.save()
    if order_checkout.save() and s.save():
        send_msg_checkout.delay(email=user.email, name=user.name)
        return jsonify({"message" : "Successfully checked out"})
    else :
        return jsonify({"message" : "Error occured, try again."})

@users_api_blueprint.route('/me/order_history', methods=['GET'])
@jwt_required
def order_history():
    user_id = get_jwt_identity()
    user = User.get_or_none(User.id == user_id)
    order_checkouts = OrderCheckout.select().where(OrderCheckout.user == user.id)
    if order_checkouts :
        return jsonify([{"id" : o.id, "subscription_recipe" : o.subscription_recipe.recipe.recipe_name, "user" : o.user.id, "created_at" : o.created_at, "recipe_image_path" : app.config.get("S3_LOCATION") + o.subscription_recipe.recipe.image_url} for o in order_checkouts])
    else :
        return jsonify({"messages" : "User does not have any previous order yet"})