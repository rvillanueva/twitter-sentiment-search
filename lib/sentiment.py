from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def getSentimentKey(item):
    return item['sentiment']['compound']

def analyzeTweets(tweets):
    for tweet in tweets:
      tweet['sentiment'] = analyzer.polarity_scores(tweet['text'])
    tweets = sorted(tweets, key=getSentimentKey, reverse=True)
    print(tweets)
    return tweets
