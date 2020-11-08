from models.base_model import BaseModel
from models.user import User 
from models.subscription_recipe import Subscription_Recipe
import peewee as pw

class OrderCheckout(BaseModel):
    subscription_recipe = pw.ForeignKeyField(Subscription_Recipe, backref = "subscription_recipes", on_delete = "CASCADE")
    user = pw.ForeignKeyField(User, backref = "subscription_recipes", on_delete = "CASCADE")