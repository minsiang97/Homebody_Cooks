from models.base_model import BaseModel
from models.user import User 
from models.subscription import Subscription
from models.recipe import Recipe
from models.ingredient import Ingredient 
import peewee as pw

class Subscription_Recipe(BaseModel):
    user = pw.ForeignKeyField(User, backref = "recipes", on_delete="CASCADE")
    subscription = pw.ForeignKeyField(Subscription, backref = "recipes", on_delete = "CASCADE")
    recipe = pw.ForeignKeyField(Recipe, backref = "recipes", on_delete = "CASCADE")
    is_checkedout = pw.BooleanField(default = 0)

