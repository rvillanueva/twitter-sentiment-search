from datetime import datetime
from urllib import parse
from application_only_auth import Client
import config

client = Client(config.twitter_consumer_key, config.twitter_consumer_secret)

def getTweets(q, cycles):
  res = {'statuses': []};
  earliest = datetime.now()
  for i in range(cycles):
    callRes = getTweetsSingleCycle(q=q, untilDate=earliest)
    if(hasattr(res, 'search_metadata') == False):
      res['search_metadata'] = callRes['search_metadata']
    res['statuses'] = res['statuses'] + callRes['statuses']
    earliest = getEarliestTweetDate(tweets=res['statuses'])
  return res

def getOneTweet(tweetId):
  query = { 'id': tweetId }
  qs = parse.urlencode(query)
  url = 'https://api.twitter.com/1.1/statuses/show.json?' + qs
  print(url)
  return client.request(url)

def getTweetsSingleCycle(q, untilDate):
    query = { 'q': q, 'count': 100}
    if untilDate:
      query['until'] = str(untilDate.year) + '-' + str(untilDate.month) + '-' + str(untilDate.day)
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
