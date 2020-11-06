from dotenv import load_dotenv
load_dotenv()
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
from models.subscription_recipe import Subscription_Recipe
from datetime import date, timedelta
from tasks import make_celery
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect
import braintree
from flask_mail import Mail, Message
from celery.schedules import crontab


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'homebody_cooks_web')

app = Flask('HOMEBODY COOKS', root_path=web_dir)
admin = Admin(app, index_view = MyAdminIndexView())
csrf = CSRFProtect(app)
celery = make_celery(app)

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

@celery.task
def send_message_create_user(email, name):
    msg = Message('Account Confirmation', recipients=[email])
    msg.body = "Hi {}. Your account has been set up successfully. You can start choosing the meals provided in your subscription plan. Start cooking and enjoy!".format(name)
    mail.send(msg)

@celery.task
def send_msg_checkout(email, name):
    msg = Message('Order Confirmation', recipients=[email])
    msg.body = "Hi {}. Your order is confirmed and will be processed immediately".format(name)
    mail.send(msg)

@celery.task
def reminder_friday():
    user_recipes = Subscription_Recipe.select().where(Subscription_Recipe.created_at.between(date.today() - timedelta(days = 5), date.today()))
    user_id = [u.user.id for u in user_recipes]
    to_send_email_id = User.select().where(User.id.not_in(user_id))
    to_send_email_list_friday = [u.email for u in to_send_email_id]
    for email in to_send_email_list_friday:
        msg = Message('Meals Reminder', recipients=[email])
        msg.body = "Hi! We noticed that you have not complete selecting your meals for the following week. Last order will be Sunday 2359."
        mail.send(msg)


@celery.task
def reminder_sunday():
    user_recipes = Subscription_Recipe.select().where(Subscription_Recipe.created_at.between(date.today() - timedelta(days = 7), date.today()))
    user_id = [u.user.id for u in user_recipes]
    to_send_email_id = User.select().where(User.id.not_in(user_id))
    to_send_email_list_sunday = [u.email for u in to_send_email_id]
    for email in to_send_email_list_sunday:
        msg = Message('Meals Reminder', recipients=[email])
        msg.body = "Hi! We noticed that you have not complete selecting your meals for the following week. Last order will be Today 2359."
        mail.send(msg)

celery.conf.timezone = 'Asia/Kuala_Lumpur'

celery.conf.beat_schedule = {
    "run-me-every-friday-nineam": {
    "task": "app.reminder_friday",
    "schedule": crontab(hour=9, minute=00, day_of_week=5)
    }
}

celery.conf.beat_schedule = {
    "run-me-every-sunday-nineam": {
    "task": "app.reminder_sunday",
    "schedule": crontab(hour=9, minute=00, day_of_week=0)
    }
}

