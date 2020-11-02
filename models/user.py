from models.base_model import BaseModel
from models.subscription import Subscription
import peewee as pw
from werkzeug.security import generate_password_hash
import re

class User(BaseModel):
    name = pw.CharField(unique=False, null = False)
    email = pw.CharField(unique=True, null = False)
    password_hash = pw.CharField(unique=False, null = False)
    password = None
    is_valid = pw.BooleanField(default=0)
    subscription = pw.ForeignKeyField(Subscription, backref="users", on_delete="CASCADE", default=1)

    def validate(self):
        duplicate_emails = User.get_or_none(User.email == self.email)

        if duplicate_emails and self.id != duplicate_emails.id:
            self.errors.append('Email registered. Try using another email.')
        
        if self.password:
            if len(self.password)<6:
                self.errors.append("Password must be at least 6 characters.")
            
            if not re.search("[a-z]", self.password):
                self.errors.append("Password must include lowercase.")
            
            if not re.search("[A-Z]", self.password):
                self.errors.append("Password must include uppercase.")
            
            if not re.search("[\*\^\%\!\@\#\$\&]", self.password):
                self.errors.append("Password must include special characters.")
            
            if len(self.errors) == 0:
                self.password_hash = generate_password_hash(self.password)
            
        if not self.password_hash:
            self.errors.append("Password must be present")
        
    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
    