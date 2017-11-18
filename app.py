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
    analyzed = sentiment.analyzeStatuses(statuses=res['statuses'])
    res['statuses'] = sentiment.sortStatusesBySentiment(analyzed)
    if(len(res['statuses']) > 100):
      res['statuses'] = res['statuses'][0:100]
    res['statuses'] = predict.batchPredictStatuses(statuses=res['statuses'])
    res['statuses'] = predict.mergePredictions(statuses=res['statuses'])
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
    predict.train()
    return 'OK', 200

def addPredictionToStatuses(statuses):
  for status in statuses:
      response = client.predict(
          MLModelId=config.aws_ml_model,
          Record=predict.getRecordFromTweet(tweet=status['tweet']),
          PredictEndpoint=config.aws_ml_endpoint
      )
      status['prediction'] = response;
  return statuses

if __name__ == '__main__':
    app.run()
