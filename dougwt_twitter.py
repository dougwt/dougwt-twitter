import urllib
import urllib2
import json
import os.path
import time


def fetch_tweets(username, quantity=1, cache_expiration=60):
    """Returns a list of a user's most recent tweets in the form
    of dictionaries"""

    cache_file = 'dougwt_twitter_cache'

    # format the proper url for the api call
    url = 'https://api.twitter.com/1/statuses/user_timeline.json?'
    url_attr = {'include_entities'  : 'true',
                'include_rts'       : 'false',
                'exclude_replies'   : 'true',
                'screen_name'       : username,
                'count'             : quantity
            }

    cache_file = os.path.dirname(__file__) + '/' + cache_file
    timenow = int(time.time())
    
    if os.path.isfile(cache_file):
        # read cache_file's timestamp if it exists
        timestamp = int(os.path.getmtime(cache_file))
        expired = timestamp + cache_expiration
    else:
        # uh oh cache_file doesn't exist
        timestamp = 0
        expired = 0

    if timenow < expired:
        # fetch the json string from cache
        cache = file(cache_file, 'r')
        json_string = cache.read()
        cache.close
    else:
        # fetch the json string using twitter's api
        url += urllib.urlencode(url_attr)
        json_string = urllib2.urlopen(url).read()
       
        try:
            # cache the json string for later
            cache = file(cache_file, 'w')
            cache.write(json_string)
            cache.close
        except IOError:
            print 'Error: Unable to write to', cache_file

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
