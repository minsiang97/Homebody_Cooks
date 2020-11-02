from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=False)
    email = pw.CharField(unique=True)
    password_hash = pw.CharField(unique=False)

    def validate(self):
        duplicate_user_email = User.get_or_none(User.email == self.email)

        if duplicate_user_email and self.id != duplicate_user_email.id:
            self.errors.append('Email already exist')
        
        def is_active(self):
        
        return True

    def get_id(self):
        
        return self.id

    def is_authenticated(self):
        
        return self.authenticated

    def is_anonymous(self):
        
        return False
    