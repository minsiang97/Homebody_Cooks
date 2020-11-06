from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from flask_login import login_required, current_user, login_user
from models.subscription import Subscription
from models.user import User
import braintree
from helpers import gateway
from app import app



subscriptions_blueprint = Blueprint('subscriptions',
                            __name__,
                            template_folder='templates')


@subscriptions_blueprint.route('/show', methods=["GET"])
def show():
    subscription_plan = Subscription.select()
    return render_template('subscriptions/show.html', subscription_plan = subscription_plan)

@subscriptions_blueprint.route('/show/update', methods=["GET"])
def show_update():
    subscription_plan = Subscription.select()
    return render_template('subscriptions/show_update.html', subscription_plan = subscription_plan)

@subscriptions_blueprint.route('/<plan_id>/', methods=["POST"])
@login_required
def create(plan_id):
    subscription_plan = Subscription.get_by_id(plan_id)
    user = User.get_by_id(current_user.id)
    user.subscription = subscription_plan
    if user.save():
        flash('Plan Selected')
        return redirect(url_for('transactions.new_checkout', subscription_id = subscription_plan.id))
    else:
        flash("An error occured")
        return render_template('subscriptions/show.html', subscription_plan = subscription_plan)

@subscriptions_blueprint.route('/<plan_id>/change_plan', methods=["POST"])
@login_required
def update(plan_id):
    subscription_plan = Subscription.get_by_id(plan_id)
    user = User.get_by_id(current_user.id)
    result = gateway.subscription.update(str(current_user.id), {
        "price" : subscription_plan.price,
        "plan_id" : subscription_plan.id,
        })
    
    if result.is_success :
        user.subscription = subscription_plan
        
        if user.save():
            flash("Plan changed successfully", "success")
            return redirect(url_for('home'))
        else :
            flash("Failed to change plan", "danger")
            return redirect(url_for('subscriptions.show'))
    
    else :
        flash("Failed to change plan", "danger")
        return redirect(url_for('subscriptions.show'))
