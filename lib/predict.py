import config
import boto3, json

session = boto3.Session(
    aws_access_key_id=config.aws_access_key,
    aws_secret_access_key=config.aws_access_secret,
    region_name=config.aws_region
)

dynamodb_client = session.client('dynamodb')

def addLabeledTweet(tweet, label):
    dynamodb_client.put_item(TableName=config.aws_dynamodb_tablename, Item={
      '_id': {
        'S': str(tweet['id'])
      },
      'label': {
        'S': label
      },
      'tweet': {
        'S': json.dumps(tweet)
      }
    })
    return

def train():
    return
