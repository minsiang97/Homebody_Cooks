from app import app
from flask import render_template
from homebody_cooks_web.blueprints.users.views import users_blueprint
from homebody_cooks_web.blueprints.sessions.views import sessions_blueprint
from homebody_cooks_web.blueprints.transactions.views import transactions_blueprint
from homebody_cooks_web.blueprints.subscriptions.views import subscriptions_blueprint
from homebody_cooks_web.blueprints.recipes.views import recipes_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(transactions_blueprint, url_prefix="/subscription/<subscription_id>/transactions")
app.register_blueprint(subscriptions_blueprint, url_prefix="/subscriptions")
app.register_blueprint(recipes_blueprint, url_prefix="/recipes")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')
