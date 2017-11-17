import config, sentiment
import boto3, json

session = boto3.Session(
    aws_access_key_id=config.aws_access_key,
    aws_secret_access_key=config.aws_access_secret,
    region_name=config.aws_region
)

dynamodb_client = session.client('dynamodb')
s3_client = session.client('s3')
ml_client = boto3.client('machinelearning')

def addLabeledTweet(tweet, label):
    dynamodb_client.put_item(TableName=config.aws_dynamodb_tablename, Item={
      '_id': {
        'S': str(tweet['id'])
      },
      'label': {
        'N': label
      },
      'tweet': {
        'S': json.dumps(tweet)
      }
    })
    return

def train():
    __writeDynamoToS3()
    __trainMachineLearning()
    return

def predictTweet(tweet):
  ml_client.predict(MLModelId='tweet_classifier')

def __getFeaturesFromTweet(tweet):
  sentiment = sentiment.getSentiment(text=tweet['text'])
  res = [
    sentiment['neg'],
    sentiment['neu'],
    sentiment['pos'],
    sentiment['compound'],
    tweet['retweet_count'],
    tweet['favorite_count'],
    tweet['user']['followers_count'],
    tweet['user']['friends_count']
  ]
  return res

def __getFeatureHeaders():
  return [
    'negSentiment',
    'neuSentiment',
    'posSentiment',
    'compoundSentiment',
    'retweetCount',
    'favoriteCount',
    'userFollowerCount',
    'userFriendCount'
  ]


def __writeDynamoToS3():
  string = ''
  rows = []
  headers = __getFeatureHeaders()
  headers.append('label')
  rows.append(headers)

  items = dynamodb_client.query(TableName=config.aws_dynamodb_tablename)
  for item in items:
    cols = __getFeaturesFromTweet(tweet=item['tweet'])
    cols.append(item['label'])
    rows.append(cols)

  for row, r in enumerate(rows):
    for col, c in enumerate(row):
      string += row
      if(r != len(rows) - 1):
        string += ','
    if(c != len(row) - 1):
      string += '\n'

  obj = s3_client.put_object(Body=string, Bucket=config.aws_s3_bucket, Key='data/training.csv')

def __trainMachineLearning():
  datasource = ml_client.create_datasource_from_s3(
    DataSourceId='tweet_sentiment_data',
    DataSourceName='Tweet Sentiment Data',
    DataSpec={ 'DataLocationS3': config.aws_s3_bucket + '/data/training.csv' }
  )
  ml_client.create_ml_model(
    MLModelId='tweet_classifier',
    MLModelType='BINARY'
  )
