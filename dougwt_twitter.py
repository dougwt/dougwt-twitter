import urllib
import urllib2
import json

def fetch_tweets(username, quantity):
    """Returns a list of a user's most recent tweets in the form
    of dictionaries"""

    # format the proper url for the api call
    url = 'https://api.twitter.com/1/statuses/user_timeline.json?'
    url_attr = {'include_entities'  : 'true',
                'include_rts'       : 'false',
                'exclude_replies'   : 'true',
                'screen_name'       : username,
                'count'             : quantity
            }

    # fetch the json data using twitter's api
    url += urllib.urlencode(url_attr)
    json_string = urllib2.urlopen(url).read()
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
    print fetch_tweets('dougwt', 1)

if __name__ == "__main__":
    main()
