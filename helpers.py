import boto3, botocore
from app import app
import braintree
from authlib.integrations.flask_client import OAuth

s3 = boto3.client(
  "s3",
  aws_access_key_id=app.config.get("S3_KEY"),
  aws_secret_access_key=app.config.get("S3_SECRET")
)

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=app.config.get("BT_MERCHANT_ID"),
        public_key=app.config.get("BT_KEY"),
        private_key=app.config.get("BT_SECRET")
    )
)

oauth = OAuth()

oauth.register('google',
    client_id=app.config.get("GOOGLE_CLIENT_ID"),
    client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'token_endpoint_auth_method': 'client_secret_basic',
        'token_placement': 'header',
        'prompt': 'consent'
    }
)

oauth.init_app(app)

def upload_to_s3(file, folder_name, acl="public-read"):
  try:
    s3.upload_fileobj(
      file,
      app.config.get("S3_BUCKET"),
      f"user-{folder_name}/{file.filename}",
      ExtraArgs={
        "ACL": acl,
        "ContentType": file.content_type
      }
    )

  except Exception as e:
    # This is a catch all exception, edit this part to fit your needs.
    print("Something Happened: ", e)
    return e

  return f"user-{folder_name}/{file.filename}"


def get_client_token():
  return gateway.client_token.generate()

def create_transaction(amount, nonce):
  return gateway.transaction.sale({
      "amount": amount,
      "payment_method_nonce": nonce,
      "options": {
        "submit_for_settlement": True
      }
  })
