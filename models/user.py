from models.base_model import BaseModel
from models.subscription import Subscription
import peewee as pw
from werkzeug.security import generate_password_hash
import re
from playhouse.hybrid import hybrid_property
from flask_admin import Admin, AdminIndexView
from flask_login import current_user, UserMixin
from flask import abort, flash


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False, null = False)
    email = pw.CharField(unique=True, null = False)
    password_hash = pw.CharField(unique=False, null = False)
    password = None
    is_valid = pw.BooleanField(default=0)
    subscription = pw.ForeignKeyField(Subscription, backref="users", on_delete="CASCADE", null = True)
    profile_image_url = pw.TextField(default="users/Untitled_Artwork.jpg")
    is_admin = pw.BooleanField(default=0)

    @hybrid_property
    def profile_image_path(self):
        from app import app
        if self.profile_image_url:
            return app.config.get("S3_LOCATION") + self.profile_image_url
        else:
            return app.config.get("S3_LOCATION") + "Untitled_Artwork.jpg"
            

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
    
    def delete_from_cart(self,recipe):
        from models.subscription_recipe import Subscription_Recipe
        import datetime
        return Subscription_Recipe.delete().where(Subscription_Recipe.user == self.id, Subscription_Recipe.recipe==recipe.id, Subscription_Recipe.created_at >= datetime.date.today()).execute()


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin
        else :
            return current_user.is_authenticated
        