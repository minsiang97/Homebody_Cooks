from models.base_model import BaseModel
import peewee as pw
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.measurement import Measurement

class RecipeIngredient(BaseModel):
    recipe_id = pw.ForeignKeyField(Recipe, backref="ingredients", on_delete = "CASCADE")
    ingredient_id = pw.ForeignKeyField(Ingredient, backref="ingredients", on_delete = "CASCADE")
    measurement_id = pw.ForeignKeyField(Measurement, backref="ingredients", on_delete = "CASCADE")
    amount = pw.CharField()


