from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def analyzeTweets(tweets):
    for tweet in tweets:
      tweet['sentiment'] = analyzer.polarity_scores(tweet['text'])
    return tweets

def sortTweetsBySentiment(tweets):
    tweets = sorted(tweets, key=__getSentimentKey, reverse=True)
    return tweets

def getSentiment(text):
  return analyzer.polarity_scores(text)

def __getSentimentKey(item):
    return item['sentiment']['compound']
