import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    S3_BUCKET                 = os.environ.get("S3_BUCKET_NAME")
    S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET                 = os.environ.get("S3_SECRET_KEY")
    AWS_S3_DOMAIN             = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

    BT_MERCHANT_ID            = os.environ.get("BT_MERCHANT_ID")
    BT_KEY                    = os.environ.get("BT_KEY")
    BT_SECRET                 = os.environ.get("BT_SECRET")
    MAILGUN_API               = os.environ.get("MAILGUN_API")

    GOOGLE_CLIENT_ID          = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET      = os.environ.get("GOOGLE_CLIENT_SECRET")

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
