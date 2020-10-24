from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.image import Image
from models.user import User
from models.transaction import Transaction
from helpers import get_client_token, create_transaction
from braintree.successful_result import SuccessfulResult
from flask_login import current_user
import requests

transactions_blueprint = Blueprint('transactions',
                            __name__,
                            template_folder='templates')

@transactions_blueprint.route('/new', methods=['GET'])
def new(image_id):
  return render_template('transactions/new.html', client_token=get_client_token(), image_id=image_id)

@transactions_blueprint.route('/', methods=['POST'])
def create(image_id):
  data = request.form
  image = Image.get_by_id(image_id)

  result = create_transaction(data.get("amount"), data.get("payment_method_nonce"))
  print(type(result))
  if type(result) == SuccessfulResult:
    new_transaction = Transaction(amount=data.get("amount"), image=image, user_id=current_user.id)
    if new_transaction.save():
      from app import app
      requests.post(
        "https://api.mailgun.net/v3/sandboxc2532b7ddfbc4302aa61f8c427bf85d1.mailgun.org/messages",
        auth=("api", app.config.get("MAILGUN_API") ),
        data={"from": "Mailgun Sandbox <postmaster@sandboxc2532b7ddfbc4302aa61f8c427bf85d1.mailgun.org>",
          "to": "Ming Hao Chan <minghaochan.2018@gmail.com>",
          "subject": "Hello Ming Hao Chan",
          "text": "Successfully received a donation"})

      return redirect(url_for("users.show", username=image.user.username ))
    else:
      return "Could not save transaction"
  else:
    return "Could not create braintree transaction"