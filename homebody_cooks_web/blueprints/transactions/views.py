from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from models.user import User
from models.subscription import Subscription
from models.transaction import Transaction
import braintree
from app import TRANSACTION_SUCCESS_STATUSES, app
from flask_login import login_required, current_user
from helpers import gateway
from braintree.successful_result import SuccessfulResult

transactions_blueprint = Blueprint('transactions',
                            __name__,
                            template_folder='templates')



@transactions_blueprint.route('/new', methods = ["GET"])
def new_checkout(subscription_id):
    subscription = Subscription.get_or_none(Subscription.id == subscription_id)
    client_token = gateway.client_token.generate()
    return render_template('transactions/new.html',client_token = client_token, subscription = subscription)


@transactions_blueprint.route('/<transaction_id>', methods = ["GET"])
def show_checkout(subscription_id, transaction_id):
    subscription = Subscription.get_or_none(Subscription.id == subscription_id)
    transaction = gateway.transaction.find(transaction_id)
    user = User.get_by_id(current_user.id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES :
        result = {
            'header' : "Transaction Successful",
            'icon' : "success",
            'message' : "Your transaction has been successfully processed."
        }
        user.is_valid = True
        user.save()

    else :
        result = {
            'header' : "Transaction Failed",
            'icon' : "failed",
            'message' : "Your transaction cannot be processed"
        }
    return render_template("transactions/show.html", transaction = transaction, result = result, subscription = subscription)

@transactions_blueprint.route("/", methods=["POST"])
def create_checkout(subscription_id):
    subscription = Subscription.get_or_none(Subscription.id == subscription_id)
    nonce_from_the_client = request.form["payment_method_nonce"]
    result = gateway.customer.create({
        "first_name": current_user.name,
        "email": current_user.email,
        "payment_method_nonce": nonce_from_the_client
    })
    
    if result.is_success :
        result_subscription = gateway.subscription.create({
            "id" : current_user.id,
            "payment_method_token": result.customer.payment_methods[0].token,
            "plan_id": subscription.id
        })

    if type(result_subscription) == SuccessfulResult:
        new_transaction = Transaction(amount = subscription.price, subscription = subscription.id , user = current_user.id)
    
        if new_transaction.save():
            flash ("Transaction Successful", "success")
            return redirect(url_for('home'))

    else :
        flash ("Transaction Failed, check your card details and try again", "danger")
        return redirect(url_for('home'))    


