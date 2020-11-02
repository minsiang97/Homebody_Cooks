from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from flask_login import login_required, current_user, login_user
from models.subscription import Subscription
from models.user import User



subscriptions_blueprint = Blueprint('subscriptions',
                            __name__,
                            template_folder='templates')


@subscriptions_blueprint.route('/show', methods=["GET"])
def show():
    subscription_plan = Subscription.select()
    return render_template('subscriptions/show.html', subscription_plan = subscription_plan)

@subscriptions_blueprint.route('/<plan_id>/', methods=["POST"])
@login_required
def create(plan_id):
    subscription_plan = Subscription.get_by_id(plan_id)
    user = User.get_by_id(current_user.id)
    user.subscription = subscription_plan
    if user.save():
        flash('Plan Selected')
        return redirect(url_for('home'))
    else:
        flash("An error occured")
        return render_template('subscriptions/show.html', subscription_plan = subscription_plan)

