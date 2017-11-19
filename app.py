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
    try:
        secret = request.headers['X-Auth-Secret']
    except:
        secret = None

    res = twitter.getTweets(q = request.args['q'], cycles = cycles)
    analyzed = sentiment.analyzeStatuses(statuses=res['statuses'])
    res['statuses'] = sentiment.sortStatusesBySentiment(analyzed)
    if(len(res['statuses']) > 100):
        res['statuses'] = res['statuses'][0:100]
    if(secret == config.auth_secret):
        res['statuses'] = predict.batchPredictStatuses(statuses=res['statuses'])
    res['statuses'] = predict.mergePredictions(statuses=res['statuses'])
    res['statuses'] = predict.sortStatusesByScore(statuses=res['statuses'])
    return jsonify(res), 200

@app.route('/api/label', methods=['post'])
def addLabel():
    try:
      secret = request.headers['X-Auth-Secret']
    except:
      secret = None
    if(secret != config.auth_secret):
        return 'FORBIDDEN', 403
    body = request.get_json()
    tweet = twitter.getOneTweet(tweetId=body['tweetId'])
    predict.addLabeledTweet(tweet=tweet, label=body['label'])
    return 'OK', 200

if __name__ == '__main__':
    app.run()
