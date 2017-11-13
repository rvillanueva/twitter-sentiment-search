from flask import Flask, render_template, jsonify, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from urllib import parse
from application_only_auth import Client
import os

import imp
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
analyzer = SentimentIntensityAnalyzer()
client = Client(twitter_consumer_key, twitter_consumer_secret)

@app.route('/')
def index():
    return render_template('index.html')

# API
@app.route('/api/posts', methods=['get'])
def returnPosts():
    res = getTweets(q = request.args['q'])
    res['statuses'] = analyzeTweetSentiments(res['statuses'])
    return jsonify(res)

def getTweets(q):
  query = { 'q': q, 'count': 100}
  qs = parse.urlencode(query)
  url = 'https://api.twitter.com/1.1/search/tweets.json?' + qs
  return client.request(url)

def analyzeTweetSentiments(tweets):
    for tweet in tweets:
      tweet['sentiment'] = analyzer.polarity_scores(tweet['text'])
    tweets = sorted(tweets, key=getSentimentKey, reverse=True)
    return tweets

def getSentimentKey(item):
  return item['sentiment']['compound']

class SentimentTweet:
      def __init__(self):
        super(MySubClassBetter, self).__init__()

if __name__ == '__main__':
    app.run()
