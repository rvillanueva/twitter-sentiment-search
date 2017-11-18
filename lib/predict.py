import config
from lib import sentiment
import boto3, json
from datetime import datetime

session = boto3.Session(
    aws_access_key_id=config.aws_access_key,
    aws_secret_access_key=config.aws_access_secret,
    region_name=config.aws_region
)

dynamodb_client = session.client('dynamodb')
s3_client = session.client('s3')
ml_client = session.client('machinelearning')

def addLabeledTweet(tweet, label):
    if(label == 'good'):
      binaryLabel = '1'
    elif(label == 'bad'):
      binaryLabel = '0'
    else:
      return
    dynamodb_client.put_item(TableName=config.aws_dynamodb_tablename, Item={
      '_id': {
        'S': str(tweet['id'])
      },
      'label': {
        'N': binaryLabel
      },
      'tweet': {
        'S': json.dumps(tweet)
      }
    })
    return

def train():
    __writeDynamoToS3()
    return

def predictTweet(tweet):
  record = {}
  props = __getFeatureHeaders
  features = __getFeaturesFromTweet(tweet)
  for prop, p in enumerate(props):
    record[prop] = features[p]
  ml_client.predict(
    MLModelId='tweet_classifier',
    Record=record,
    PredictEndpoint=config.aws_ml_endpoint
  )

def getRecordFromTweet(tweet):
  record = {}
  features = __getFeaturesFromTweet(tweet)
  headers = __getFeatureHeaders()
  for header, h in enumerate(headers):
    record[header] = features[h]
  return record

def __getFeaturesFromTweet(tweet):
  analyzed = sentiment.getSentiment(text=tweet['text'])
  res = [
    tweet['id'],
    tweet['text'],
    analyzed['neg'],
    analyzed['neu'],
    analyzed['pos'],
    analyzed['compound'],
    tweet['retweet_count'],
    tweet['favorite_count'],
    tweet['user']['followers_count'],
    tweet['user']['friends_count']
  ]
  return res

def __getFeatureHeaders():
  return [
    'id',
    'text',
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

  items = dynamodb_client.scan(TableName=config.aws_dynamodb_tablename)['Items']
  for item in items:
    tweet = json.loads(item['tweet']['S'])
    cols = __getFeaturesFromTweet(tweet=tweet)
    cols.append(item['label']['N'])
    rows.append(cols)

  for r, row in enumerate(rows):
    for c, col in enumerate(row):
      string += str(col)
      if(c != len(row) - 1):
        string += ','
    if(c != len(rows) - 1):
      string += '\n'
  obj = s3_client.put_object(Body=string, Bucket=config.aws_s3_bucket, Key='data/training.csv')



## UNUSED
def __trainMachineLearning():
  datasource = ml_client.create_datasource_from_s3(
    DataSourceId='tweet_sentiment_data-' + str(datetime.now().valueof()),
    DataSourceName='Tweet Sentiment Data',
    DataSpec={
      'DataRearrangement': 'string',
      'DataSchema': {
        "targetFieldName": "label",
        "dataFormat": "CSV",
        "dataFileContainsHeader": True,
        "attributes": [
            { "fieldName": "id", "fieldType": "CATEGORICAL" },
            { "fieldName": "text", "fieldType": "TEXT" },
            { "fieldName": "negSentiment", "fieldType": "NUMBER" },
            { "fieldName": "neuSentiment", "fieldType": "NUMBER" },
            { "fieldName": "posSentiment", "fieldType": "NUMBER" },
            { "fieldName": "compoundSentiment", "fieldType": "NUMBER" },
            { "fieldName": "retweetSentiment", "fieldType": "NUMBER" },
            { "fieldName": "favoriteCount", "fieldType": "NUMBER" },
            { "fieldName": "userFollowerCount", "fieldType": "NUMBER" },
            { "fieldName": "userFriendCount", "fieldType": "NUMBER" },
            { "fieldName": "label", "fieldType": "BINARY" }
        ]
      },
      'DataSchemaLocationS3': config.aws_s3_bucket + '/data/training.csv'
    }
  )
  ml_model = ml_client.create_ml_model(
    MLModelId='twitter-sentiment-search_' + str(datetime.now().timestamp()),
    MLModelType='BINARY',
    TrainingDataSourceId=datasource['DataSourceId']
  )
  #models = dynamodb_client.scan(TableName=config.aws_dynamodb_tablename)['Items']
