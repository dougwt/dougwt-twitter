import urllib
import urllib2
import json
import os.path
import time


def fetch_tweets(username, quantity=1, cache_expiration=60):
    """Returns a list of a user's most recent tweets in the form
    of dictionaries"""

    DEBUG = False

    # format the proper url for the api call
    url = 'https://api.twitter.com/1/statuses/user_timeline.json?'
    url_attr = {'include_entities'  : 'true',
                'include_rts'       : 'false',
                'exclude_replies'   : 'true',
                'screen_name'       : username,
                'count'             : quantity
            }

    timestamp = int(os.path.getmtime('dougwt_twitter_cache'))
    expired = timestamp + cache_expiration
    timenow = int(time.time())

    if DEBUG:
        print 'Timestamp : %d' % timestamp
        print 'Expired   : %d' % expired 
        print 'Currently : %d' % timenow

    if timenow < expired:
        # fetch the json string from cache
        cache = file('dougwt_twitter_cache', 'r')
        json_string = cache.read()
        cache.close
        
        if DEBUG:
            print 'CACHE'
    else:
        # fetch the json string using twitter's api
        url += urllib.urlencode(url_attr)
        json_string = urllib2.urlopen(url).read()
       
        # cache the json string for later
        cache = file('dougwt_twitter_cache', 'w')
        cache.write(json_string)
        cache.close
        
        if DEBUG:
            print 'API'

    # convert the json_string into an object
    json_data = json.loads(json_string)

    # gather the relevant information from each tweet
    tweets = []
    for single_tweet in json_data:
        text = single_tweet['text']
        created = single_tweet['created_at']
        id = single_tweet['id_str']
        url = 'http://twitter.com/' + username + '/status/' + id + '/' 

        tweets.append({'text':text, 'created':created, 'url':url})

    return tweets


def main():
    print fetch_tweets('dougwt')

if __name__ == "__main__":
    main()
