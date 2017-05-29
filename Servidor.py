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
from Token_Dropbox import token
from Token_Twitter import consumer_key, consumer_secret, access_key, access_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
dbx = dropbox.Dropbox(token)
user = dbx.users_get_current_account()
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:1024")

def subir_a_Dropbox(name):
    with open(name, "rb") as f:
        data = f.read()
        f.close()
    fname = "/"+name
    try:
        dbx.files_upload(data, fname, mute=False)
        print("Subido a Dropbox "+name)
    except:
        print("Error al subir a Dropbox "+name)

class Listener(StreamListener):
    def on_data(self, data):
        currenttime = datetime.now()
        diff = currenttime - Listener.inicio
        namefile=current_thread().name+".json"
        #print(namefile+"   "+str(diff.total_seconds()))
        diffmin = diff.total_seconds()/60
        if diffmin<Listener.limit:
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
        l = Listener()
        stream = Stream(auth, l)
        stream.filter(track=[self.hashtag])
        stream.disconnect()
        name = current_thread().name+".json"
        subir_a_Dropbox(name)
        os.remove(name)
        self.queue.task_done()

if __name__ == "__main__":
    vector = socket.recv_json()
    print(vector)
    tiempo = vector[len(vector)-1]
    Listener.inicio = datetime.now()
    Listener.limit = float(tiempo)
    #print (Listener.inicio)
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

    subir_a_Dropbox('Common.json')
    os.remove('Common.json')

    socket.send_json(vector)
