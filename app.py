import os
import config
from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.peewee import ModelView
from models.base_model import db
from models.user import User, MyAdminIndexView
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.recipe_ingredient import RecipeIngredient
from models.measurement import Measurement
from models.subscription import Subscription
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import braintree
from flask_mail import Mail
from flask_jwt_extended import JWTManager

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'homebody_cooks_web')

app = Flask('HOMEBODY COOKS', root_path=web_dir)
admin = Admin(app, index_view = MyAdminIndexView())
csrf = CSRFProtect(app)

admin.add_view(ModelView(User))
admin.add_view(ModelView(Ingredient))
admin.add_view(ModelView(Recipe))
admin.add_view(ModelView(RecipeIngredient))
admin.add_view(ModelView(Measurement))
admin.add_view(ModelView(Subscription))

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
mail = Mail(app)
jwt = JWTManager(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

mail = Mail(app)

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.get(User.id == user_id)

@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
