from app import app, csrf
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from homebody_cooks_api.blueprints.users.views import users_api_blueprint
from homebody_cooks_api.blueprints.sessions.views import sessions_api_blueprint
from homebody_cooks_api.blueprints.recipes.views import recipes_api_blueprint
from homebody_cooks_api.blueprints.subscriptions.views import subscriptions_api_blueprint
from homebody_cooks_api.blueprints.recipe_ingredients.views import recipe_ingredients_api_blueprint

csrf.exempt(users_api_blueprint)
csrf.exempt(sessions_api_blueprint)
csrf.exempt(recipes_api_blueprint)
csrf.exempt(subscriptions_api_blueprint)
csrf.exempt(recipe_ingredients_api_blueprint)

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/sessions')
app.register_blueprint(recipes_api_blueprint, url_prefix='/api/v1/recipes')
app.register_blueprint(subscriptions_api_blueprint, url_prefix='/api/v1/subscriptions')
app.register_blueprint(recipe_ingredients_api_blueprint, url_prefix='/api/v1/recipe_ingredients')