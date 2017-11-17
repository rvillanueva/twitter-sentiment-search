import os, imp

try:
    imp.find_module('env')
    import env
    twitter_consumer_key = env.TWITTER_CONSUMER_KEY
    twitter_consumer_secret = env.TWITTER_CONSUMER_SECRET
    aws_access_key = env.AWS_ACCESS_KEY
    aws_access_secret = env.AWS_ACCESS_SECRET
    aws_dynamodb_tablename = env.AWS_DYNAMODB_TABLENAME
    aws_region = env.AWS_REGION
except ImportError:
    print('No config, using environment variables')
    twitter_consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    twitter_consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_access_secret = os.getenv('AWS_ACCESS_SECRET')
    aws_dynamodb_tablename = os.getenv('AWS_DYNAMODB_TABLENAME')
    aws_dynamodb_tablename = os.getenv('AWS_REGION')
