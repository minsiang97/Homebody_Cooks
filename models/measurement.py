from models.base_model import BaseModel
import peewee as pw

class Measurement(BaseModel):
    unit = pw.CharField(null=False)