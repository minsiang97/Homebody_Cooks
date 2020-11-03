from models.base_model import BaseModel
import peewee as pw

class Recipe(BaseModel):
    name = pw.CharField(null=False)
    description = pw.TextField(null=True)
    image_url = pw.TextField(null=True)