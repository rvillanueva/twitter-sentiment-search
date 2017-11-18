from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def analyzeStatuses(statuses):
    for status in statuses:
      status['sentiment'] = analyzer.polarity_scores(status['tweet']['text'])
    return statuses

def sortStatusesBySentiment(statuses):
    statuses = sorted(statuses, key=__getSentimentKey, reverse=True)
    return statuses

def getSentiment(text):
  return analyzer.polarity_scores(text)

def __getSentimentKey(item):
    return item['sentiment']['compound']
