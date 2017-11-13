import json, os
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib import parse
from application_only_auth import Client

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
cycles = 2
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
  res = {'statuses': []};
  earliest = datetime.now()
  for i in range(cycles):
    callRes = getTweetsSingleCycle(q=q, untilDate=earliest)
    if(hasattr(res, 'search_metadata') == False):
      res['search_metadata'] = callRes['search_metadata']
    res['statuses'] = res['statuses'] + callRes['statuses']
    earliest = getEarliestTweetDate(tweets=res['statuses'])
  if(len(res['statuses']) > 100):
    res['statuses'] = res['statuses'][0:100]
  return res

def getTweetsSingleCycle(q, untilDate):
    query = { 'q': q, 'count': 100}
    if untilDate:
      query['util'] = str(untilDate.year) + '-' + str(untilDate.month) + '-' + str(untilDate.day)
    qs = parse.urlencode(query)
    url = 'https://api.twitter.com/1.1/search/tweets.json?' + qs
    return client.request(url)

def getEarliestTweetDate(tweets):
    earliest = None
    for tweet in tweets:
        datetimeDate = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        if(earliest == None):
          earliest = datetime.now(datetimeDate.tzinfo)
        elif(datetimeDate < earliest):
            earliest = datetimeDate
    return earliest

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
