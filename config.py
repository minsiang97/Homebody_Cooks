import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    
    BT_MERCHANT_ID= os.environ.get("BT_MERCHANT_ID")
    BT_PUBLIC_KEY= os.environ.get("BT_PUBLIC_KEY")
    BT_PRIVATE_KEY= os.environ.get("BT_PRIVATE_KEY")

    S3_BUCKET                 = os.environ.get("S3_BUCKET_NAME")
    S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

    G_CLIENT_SECRET = os.environ.get("G_CLIENT_SECRET")
    G_CLIENT_ID = os.environ.get("G_CLIENT_ID")

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS =  False
    MAIL_USE_SSL =  True
    MAIL_USERNAME =  os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD =  os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER") 
    MAIL_MAX_EMAILS =  None
    MAIL_ASCII_ATTACHMENTS = False

    CELERY_BROKER_URL= os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND=os.environ.get("CELERY_RESULT_BACKEND")

    JWT_ACCESS_TOKEN_EXPIRES = False

class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
