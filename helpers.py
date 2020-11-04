import braintree
from app import app
import boto3, botocore

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id= app.config.get("BT_MERCHANT_ID"),
        public_key=app.config.get("BT_PUBLIC_KEY"),
        private_key=app.config.get("BT_PRIVATE_KEY")
    )
)

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config.get("S3_KEY"),
   aws_secret_access_key=app.config.get("S3_SECRET")
)

def upload_to_s3(file, folder_name, acl="public-read"):
  try:
    s3.upload_fileobj(
      file,
      app.config.get("S3_BUCKET"),
      f"{folder_name}/{file.filename}",
      ExtraArgs={
        "ACL": acl,
        "ContentType": file.content_type
      }
    )

  except Exception as e:
    # This is a catch all exception, edit this part to fit your needs.
    print("Something Happened: ", e)
    return e

  return f"{folder_name}/{file.filename}"