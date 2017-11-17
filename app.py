import json, os, boto3, imp
from lib import twitter, sentiment
from flask import Flask, render_template, jsonify, request
from application_only_auth import Client


try:
    imp.find_module('config')
    import config
    twitter_consumer_key = config.TWITTER_CONSUMER_KEY
    twitter_consumer_secret = config.TWITTER_CONSUMER_SECRET
    aws_access_key = os.getenv(config.AWS_ACCESS_KEY)
    aws_access_secret = os.getenv(config.AWS_ACCESS_SECRET)
except ImportError:
    twitter_consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    twitter_consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_access_secret = os.getenv('AWS_ACCESS_SECRET')
    print('No config, using environment variables')


app = Flask(__name__)
client = Client(twitter_consumer_key, twitter_consumer_secret)
cycles = 3

@app.route('/')
def index():
    return render_template('index.html')

# API
@app.route('/api/posts', methods=['get'])
def returnPosts():
    res = twitter.getTweets(q = request.args['q'], cycles = cycles, client=client)
    res['statuses'] = sentiment.analyzeTweets(res['statuses'])
    if(len(res['statuses']) > 100):
      res['statuses'] = res['statuses'][0:100]
    return jsonify(res)

class SentimentTweet:
      def __init__(self):
        super(MySubClassBetter, self).__init__()

if __name__ == '__main__':
    app.run()
