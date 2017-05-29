import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import dataset
from datetime import datetime
from threading import Thread, current_thread
from queue import *
import zmq
import json
import os
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
        currenttime = datetime.now()
        diff = currenttime - StdOutListener.inicio
        namefile=current_thread().name+".json"
        #print(namefile+"   "+str(diff.total_seconds()))
        diffmin = diff.total_seconds()/60
        if diffmin<StdOutListener.limit:
            try:
                with open('Common.json', 'a') as fg:
                    with open(namefile, 'a') as f:
                        #print(data)
                        f.write(data)
                        fg.write(data)
                        return True
                        f.close()
                        fg.close()
            except BaseException as e:
                print("Error on_data: %s" % str(e))
        else:
            return False
    def on_error(self, status):
        print (status)

class Worker(Thread):
    def __init__(self, queue, hashtag):
        self.hashtag=hashtag
        self.queue=queue
        Thread.__init__(self, name=hashtag)
    def run(self):
        name = current_thread().name+".json"
        with open(name, "a") as f:
            f.close()
        l = StdOutListener()
        stream = Stream(auth, l)
        stream.filter(track=[self.hashtag])
        stream.disconnect()
        print("Estoy subiendo a Dropbox "+self.hashtag)
        name = current_thread().name+".json"
        #print(name)
        with open(name, "rb") as f:
            data = f.read()
            f.close()
        fname = "/"+name

        #print(fname)
        try:
            dbx.files_upload(data, fname, mute=False)
            print("Subido a Dropbox "+self.hashtag)
        except:
            print("Error al subir a Dropbox "+self.hashtag)

        os.remove(name)
        self.queue.task_done()

if __name__ == "__main__":
    vector = socket.recv_json()
    print(vector)
    tiempo = vector[len(vector)-1]
    StdOutListener.inicio = datetime.now()
    StdOutListener.limit = float(tiempo)
    print (StdOutListener.inicio)
    with open('Common.json', "a") as f:
        f.close()
    nThreads=len(vector)-1
    try:
        q = Queue(nThreads)
        for i in range(nThreads):
            t = Worker(q,vector[i])
            t.start()
            q.put(t)
        q.join()
    except:
        print(" ERROR")

    with open('Common.json', "rb") as f:
        data = f.read()
        f.close()
    fname = "/Common.json"
    try:
        dbx.files_upload(data, fname, mute=False)
        print("Subido a Dropbox Common.json")
    except:
        print("Error al subir a Dropbox Common.json")
    os.remove('Common.json')

    socket.send_json(vector)
