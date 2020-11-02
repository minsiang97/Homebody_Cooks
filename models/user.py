from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=False)
    email = pw.CharField(unique=True)
    password_hash = pw.CharField(unique=False)
        
    def is_active(self):
        
        return True

    def get_id(self):
        
        return self.id

    def is_authenticated(self):
        
        return self.authenticated

    def is_anonymous(self):
        
        return False
    