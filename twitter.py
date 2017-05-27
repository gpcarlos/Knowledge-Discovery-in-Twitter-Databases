import tweepy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
def word_in_text(word, text):
    word = word.lower()
    print(text);
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)

        return True

    def on_error(self, status):
        print (status)

def process_or_store(tweet):
    print(json.dumps(tweet))

CONSUMER_KEY = 'Qs2z9VW6GOGQ9FG90BPVCFLGU'
CONSUMER_SECRET = 'DqGlTCX3VctW0lBN4LxGVIkanlqXPMznLv97ZMpSdi1xRj5xK4'
ACCESS_KEY = '515532568-QAK0DF5BCH6K1Wwp39X4kqqVRSxwEQPygAawozsk'
ACCESS_SECRET = '5vrTZsKwKxoegQ3j6LLvGQCgy2qqvU0Pu72fcZ3P2TGTn'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#l = StdOutListener()
#stream = Stream(auth, l)
#stream.filter(track=['Rajoy', 'Iglesias', 'Sánchez', 'Rivera'])

for status in tweepy.Cursor(api.search,q='java -filter:retweets').items(100):
    # Process a single status
    process_or_store(status._json) 

#search_text = "Manchester"
#search_number = 2
#search_result = api.search(search_text, rpp=search_number)
#for i in search_result:
#    print (i.text)

tweets_data_path = 'twits.txt'


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

tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)


tweets['Rajoy'] = tweets['text'].apply(lambda tweet: word_in_text('Rajoy', tweettxt))
tweets['Pedro'] = tweets['text'].apply(lambda tweet: word_in_text('Sánchez', tweettxt))
tweets['Pablo'] = tweets['text'].apply(lambda tweet: word_in_text('Iglesias', tweettxt))

#print (tweets['Rajoy'].value_counts()[True])