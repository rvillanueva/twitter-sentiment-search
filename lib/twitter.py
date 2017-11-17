from datetime import datetime
from urllib import parse

def getTweets(q, cycles, client):
  res = {'statuses': []};
  earliest = datetime.now()
  for i in range(cycles):
    callRes = getTweetsSingleCycle(q=q, untilDate=earliest, client=client)
    if(hasattr(res, 'search_metadata') == False):
      res['search_metadata'] = callRes['search_metadata']
    res['statuses'] = res['statuses'] + callRes['statuses']
    earliest = getEarliestTweetDate(tweets=res['statuses'])
  return res

def getTweetsSingleCycle(q, untilDate, client):
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
