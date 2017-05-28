import tweepy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
import dataset

from Token_Twitter import consumer_key, consumer_secret, access_key, access_secret

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        print (data)
        return True


    def on_error(self, status):
        print (status)

def process_or_store(tweet):
    print(status.text)
    #print(json.dumps(tweet))

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


q = ['#AlienCovenant']
#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
for status in tweepy.Cursor(api.search,q,lang='es').items(100):
    # Process a single status
    print(status.text)
    process_or_store(status._json)



tweets_data_path = 'python.json'


tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweettxt =tweet['text']
        tweets_data.append(tweet)
    except:
        continue

print (len(tweets_data))

tweets = pd.DataFrame()

tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
tweets['lang'] = list(map(lambda tweet: tweet['lang'], tweets_data))
tweets['country'] = list(map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else 'Undefined', tweets_data))

tweets_by_country = tweets['country'].value_counts()
#print(tweets_by_country)
for line in tweets['country']:
    print(line)
