from flask import Blueprint, jsonify
from models.recipe import Recipe
from app import app

subscription_recipes_api_blueprint = Blueprint('subscription_recipes_api',
                             __name__,
                             template_folder='templates')