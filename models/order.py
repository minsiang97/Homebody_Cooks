from models.base_model import BaseModel
from models.user import User 
from models.subscription_recipe import Subscription_Recipe
from models.recipe import Recipe
from models.ingredient import Ingredient 
import peewee as pw

class Order(BaseModel):
    subscription_recipe = pw.ForeignKeyField(Subscription_Recipe, backref = "subscription_recipes", on_delete = "CASCADE")
    ingredient = pw.ForeignKeyField(Ingredient, backref = "subscription_recipes", on_delete="CASCADE")