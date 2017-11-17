import json, config
from lib import twitter, sentiment, predict
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
cycles = 3

@app.route('/')
def index():
    return render_template('index.html')

# API
@app.route('/api/posts', methods=['get'])
def returnPosts():
    res = twitter.getTweets(q = request.args['q'], cycles = cycles)
    res['statuses'] = sentiment.analyzeTweets(res['statuses'])
    if(len(res['statuses']) > 100):
      res['statuses'] = res['statuses'][0:100]
    return jsonify(res), 200

@app.route('/api/label', methods=['post'])
def addLabel():
    body = request.get_json()
    if(request.headers['x-auth-secret'] != config.auth_secret):
        return 'FORBIDDEN', 403
    tweet = twitter.getOneTweet(tweetId=body['tweetId'])
    predict.addLabeledTweet(tweet=tweet, label=body['label'])
    return 'OK', 200

@app.route('/api/train', methods=['post'])
def train():
    train.train()
    return 'OK', 200

if __name__ == '__main__':
    app.run()
