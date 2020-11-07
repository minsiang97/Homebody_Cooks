from models.base_model import BaseModel
import peewee as pw

class Subscription(BaseModel):
    name = pw.CharField(unique=True, null=False)
    amount_of_meals = pw.IntegerField(unique=False, null=False)
    price = pw.IntegerField(null=False)