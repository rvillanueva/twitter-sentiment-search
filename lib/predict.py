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
    dataSchemaLocation = __writeDynamoToS3()
    dataSourceId = __createDataSource(dataSchemaLocation=dataSchemaLocation)['DataSourceId']
    __createMlModel(dataSourceId=dataSourceId)
    return

def batchPredictTweets(tweets):
  for t, tweet in enumerate(tweets):
    if t < 20:
      tweet['prediction'] = predictTweet(tweet=tweet)
  return tweets

def predictTweet(tweet):
  record = {}
  props = __getFeatureHeaders()
  features = __getFeaturesFromTweet(tweet)
  for p, prop in enumerate(props):
    record[prop] = str(features[p])
  return ml_client.predict(
    MLModelId=config.aws_ml_model,
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
  print('Writing from DynamoDB to S3....')
  string = ''
  key ='data/training-' + str(datetime.now().timestamp()) + '.csv'
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
      string += str(col).replace(',',' ').replace('\n', ' ')
      if(c != len(row) - 1):
        string += ','
    if(r != len(rows) - 1):
      string += '\n'
  obj = s3_client.put_object(Body=string, Bucket=config.aws_s3_bucket, Key=key)
  return config.aws_s3_bucket + '/' + key


def __createDataSource(dataSchemaLocation):
  print('Creating s3 data source from ' + dataSchemaLocation)
  datasource = ml_client.create_data_source_from_s3(
    DataSourceId='tweet_sentiment_data-' + str(datetime.now().timestamp()),
    DataSourceName='Tweet Sentiment Data, v: ' + str(datetime.now().timestamp()),
    DataSpec={
      'DataLocationS3': 's3://' + dataSchemaLocation,
      'DataSchema': json.dumps({
        "version": "1.0",
        "targetFieldName": "label",
        "dataFormat": "CSV",
        "dataFileContainsHeader": True,
        "attributes": [
            { "fieldName": "id", "fieldType": "CATEGORICAL" },
            { "fieldName": "text", "fieldType": "TEXT" },
            { "fieldName": "negSentiment", "fieldType": "NUMERIC" },
            { "fieldName": "neuSentiment", "fieldType": "NUMERIC" },
            { "fieldName": "posSentiment", "fieldType": "NUMERIC" },
            { "fieldName": "compoundSentiment", "fieldType": "NUMERIC" },
            { "fieldName": "retweetSentiment", "fieldType": "NUMERIC" },
            { "fieldName": "favoriteCount", "fieldType": "NUMERIC" },
            { "fieldName": "userFollowerCount", "fieldType": "NUMERIC" },
            { "fieldName": "userFriendCount", "fieldType": "NUMERIC" },
            { "fieldName": "label", "fieldType": "BINARY" }
        ]
      })
    },
    ComputeStatistics=True
  )
  return datasource

def __createMlModel(dataSourceId):
    print('Creating ML model from ' + dataSourceId)
    ml_model = ml_client.create_ml_model(
      MLModelId='twitter-sentiment-search_' + str(datetime.now().timestamp()),
      MLModelName='Twitter Sentiment Search, Model: ' + str(datetime.now().timestamp()),
      MLModelType='BINARY',
      TrainingDataSourceId=dataSourceId
    )
