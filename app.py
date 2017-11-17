import json, boto3, config
from lib import twitter, sentiment, train
from flask import Flask, render_template, jsonify, request
from application_only_auth import Client




app = Flask(__name__)
twitter_client = Client(config.twitter_consumer_key, config.twitter_consumer_secret)
#dynamodb_client = boto3.client('dynamodb')
cycles = 3

@app.route('/')
def index():
    return render_template('index.html')

# API
@app.route('/api/posts', methods=['get'])
def returnPosts():
    res = twitter.getTweets(q = request.args['q'], cycles = cycles, client=twitter_client)
    res['statuses'] = sentiment.analyzeTweets(res['statuses'])
    if(len(res['statuses']) > 100):
      res['statuses'] = res['statuses'][0:100]
    return jsonify(res)

@app.route('/api/label', methods=['post'])
def addTrainingPoint():
    label = request.args['label']
    tweetId = request.args['tweetId']
    #tweet = twitter.getTweet(tweetId=tweetId)
    #train.addTrainingTweet(tweet=tweet, label=label, client=dynamodb_client, tablename=config.aws_dynamodb_tablename)
    return

@app.route('/api/train', methods=['post'])
def train():
    #train.train(dynamodb_client=dynamodb_client, tablename=config.aws_dynamodb_tablename)
    return

if __name__ == '__main__':
    app.run()
