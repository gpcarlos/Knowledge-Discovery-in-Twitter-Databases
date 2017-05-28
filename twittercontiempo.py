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
from datetime import datetime

from Token_Twitter import consumer_key, consumer_secret, access_key, access_secret

def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False


class Listener(StreamListener):


    def on_data(self, data):
        currenttime = datetime.now()
        diff = currenttime - Listener.inicio
        print(diff.total_seconds())
        diffmin = diff.total_seconds()/60

        if diffmin<Listener.limit:
            try:
                with open('twitter2.json', 'a') as f:
                    #print(data)
                    f.write(data)
                    return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
        else:
            return False


    def on_error(self, status):
        print (status)
		
def process_or_store(tweet):
    print(json.dumps(tweet))

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

Listener.inicio = datetime.now()
Listener.limit = 1
print (Listener.inicio)

#l = Listener()
#stream = Stream(auth, l)
#stream.filter(track=['#PiratasDelCaribe', '#GuardianesDeLaGalaxia2', '#AlienCovenant'])
#stream.disconnect()

tweets_data_path = 'twitter.json'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweettxt =tweet['text']
        print(tweettxt)
        tweets_data.append(tweet)
    except:
        continue

print (len(tweets_data))

tweets = pd.DataFrame()


tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
tweets['lang'] = list(map(lambda tweet: tweet['lang'], tweets_data))
tweets['country'] = list(map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else 'Undefined', tweets_data))

tweets_by_country = tweets['lang'].value_counts()
#print(tweets_by_country)
for line in tweets['lang']:
    print(line)

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Idiomas', fontsize=15)
ax.set_ylabel('Numero de tweets' , fontsize=15)
ax.set_title('Top 5 Idiomas', fontsize=15, fontweight='bold')
tweets_by_country.plot(color='blue')
plt.show()

fig.savefig('temp.png', dpi=fig.dpi)

tweets['PiratesOfTheCaribbean'] = tweets['text'].apply(lambda tweet: word_in_text('Pirates of the Caribbean',tweet))
tweets['Alien'] = tweets['text'].apply(lambda tweet: word_in_text('Alien',tweet))
tweets['Guardian'] = tweets['text'].apply(lambda tweet: word_in_text('Guardian of the Galaxy',tweet))

word_in_text('piratas',pd.Series.to_string(tweets['text']))
print (tweets['text'])
prg_langs=['Pirates','Alien','Guardian']
tweets_by_prg_lang = [tweets['PiratesOfTheCaribbean'].value_counts(),
                      tweets['Alien'].value_counts(),
                      tweets['Guardian'].value_counts()]


### DE AQUÍ PARA ABAJO, CORREGIR #
x_pos = list(range(len(prg_langs)))
print(x_pos)
width = 0.8
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Numero de twits', fontsize=15)
ax.set_title('Ranking: python vs. javascript vs. ruby (Raw data)', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prg_langs)
plt.grid()
plt.show()
