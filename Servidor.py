import tweepy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import dataset
import time
from threading import Thread, current_thread
from queue import *
import zmq
import json

import dropbox
import tempfile
import shutil
from TokenDropbox import token
dbx = dropbox.Dropbox(token)
user = dbx.users_get_current_account()

from Token_Twitter import consumer_key, consumer_secret, access_key, access_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:1024")

class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            namefile=current_thread().name+".json"
            with open(namefile, 'a') as f:
                #print(data)
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
    def on_error(self, status):
        print (status)

class Worker(Thread):
    def __init__(self, queue, hashtag):
        self.hashtag=hashtag
        self.queue=queue
        Thread.__init__(self, name=hashtag)
    def run(self):
        l = StdOutListener()
        stream = Stream(auth, l)
        stream.filter(track=self.hashtag)
        #self.time.sleep(10) #tiempo en segundos
        #stream.disconnect()
        with open("twits.txt", "rb") as f:
            data = f.read()
        fname = "/"+current_thread().name+".json"
        dbx.files_upload(data, fname, mute=True)
        self.queue.task_done()

#MAIN
vector = socket.recv_json()
print(vector)
nThreads=len(vector)
try:
    q = Queue(nThreads)
    for i in range(nThreads):
        t = Worker(q,vector[i])
        t.start()
        q.put(t)
    q.join()
except:
    print("ERROR")
