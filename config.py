import os, imp

try:
    imp.find_module('env')
    import env
    auth_secret = env.AUTH_SECRET
    twitter_consumer_key = env.TWITTER_CONSUMER_KEY
    twitter_consumer_secret = env.TWITTER_CONSUMER_SECRET
    aws_access_key = env.AWS_ACCESS_KEY
    aws_access_secret = env.AWS_ACCESS_SECRET
    aws_dynamodb_tablename = env.AWS_DYNAMODB_TABLENAME
    aws_region = env.AWS_REGION
    aws_s3_bucket=env.AWS_S3_BUCKET
    aws_ml_model=env.AWS_ML_MODEL
    aws_ml_endpoint=env.AWS_ML_ENDPOINT
except ImportError:
    print('No config, using environment variables')
    auth_secret = os.getenv('AUTH_SECRET')
    twitter_consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    twitter_consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_access_secret = os.getenv('AWS_ACCESS_SECRET')
    aws_dynamodb_tablename = os.getenv('AWS_DYNAMODB_TABLENAME')
    aws_region= os.getenv('AWS_REGION')
    aws_s3_bucket=os.getenv('AWS_S3_BUCKET')
    aws_ml_model=os.getenv('AWS_ML_MODEL')
    aws_ml_endpoint=os.getenv('AWS_ML_ENDPOINT')
