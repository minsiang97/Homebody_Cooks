from models.base_model import BaseModel
import peewee as pw


class Ingredient(BaseModel):
    ingredient_name = pw.CharField(null=False)
    

    