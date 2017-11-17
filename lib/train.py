def addTrainingTweet(tweet, label, client, tablename):
  client.put_item(TableName=tablename, Item={
    _id: str(tweet.id),
    label: label,
    tweet: tweet
  })
  return

def train(dynamo_client, tablename):
  return
