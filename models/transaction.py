from models.base_model import BaseModel
from models.user import User 
from models.subscription import Subscription 
import peewee as pw

class Transaction(BaseModel):
    user = pw.ForeignKeyField(User, backref = "payment", on_delete="CASCADE")
    subscription = pw.ForeignKeyField(Subscription, backref = "payment", on_delete="CASCADE")
    amount = pw.DecimalField(decimal_places = 2)