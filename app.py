from flask import Flask, render_template, jsonify, request
import twitter, json
from urllib import parse
from application_only_auth import Client
import os

import imp
try:
    imp.find_module('config')
    import config
except ImportError:
    print('No config, using environment variables')

consumer_key = os.getenv('TWITTER_CONSUMER_KEY', config.TWITTER_CONSUMER_KEY)
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET', config.TWITTER_CONSUMER_SECRET)
client = Client(consumer_key, consumer_secret)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# API
@app.route('/api/posts', methods=['get'])
def returnPosts():
    res = getTweets(q = request.args['q'])
    return jsonify(res)

def getTweets(q):
  query = { 'q': q }
  qs = parse.urlencode(query)
  url = 'https://api.twitter.com/1.1/search/tweets.json?' + qs
  tweets = client.request(url)
  return tweets

if __name__ == '__main__':
    app.run()
