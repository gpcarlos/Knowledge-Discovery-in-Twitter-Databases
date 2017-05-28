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

import time

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

from threading import Thread
from queue import *

import zmq
import json

class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            str123='twitter2.json'
            with open(str123, 'a') as f:
                #print(data)
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))

    def on_error(self, status):
        print (status)


class Worker(Thread):
    def __init__(self, queue, name, hashtag, identify):
        self.hashtag=hashtag
        self.identify=identify
        self.queue=queue
        Thread.__init__(self, name=name)
    def run(self):
        l = StdOutListener()
        stream = Stream(auth, l)
        stream.filter(track=self.hashtag)
        self.time.sleep(10) #tiempo en segundos
        stream.disconnect()
        print("holis")
        self.queue.task_done()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:1024")

vector = socket.recv_json()
print(vector)
nThreads=len(vector)
try:
    q = Queue(nThreads)
    for i in range(nThreads):
        t = Worker(q,"T"+str(i+1),vector[i],i)
        t.start()
        q.put(t)
    q.join()
except:
    print("ERROR")
