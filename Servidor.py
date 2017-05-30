import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import dataset
from datetime import datetime
from threading import Thread, current_thread
from queue import Queue
import zmq
import json
import os
import dropbox
import tempfile
import shutil
''' IMPORTACIÓN DE TOKEN '''
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
    fname = "/%s"% name
    try:
        dbx.files_upload(data, fname, mute=False)
        print("Subido a Dropbox %s"% name)
    except:
        print("Error al subir a Dropbox %s"% name)

def Worker(term, queue):
    print("Escucho para el término '%s'" %term)
    while True:
        dato = queue.get()

        if dato == '0':
            return
        else:
            print("Imprimiendo en: "+term+".json")
            with open("%s.json" % term, "a") as f:
                f.write(dato)
            with open("Common.json", "a") as f:
                f.write(dato)

class Listener(StreamListener):
    def __init__(self, queues):
        self.queues = queues
        self.terms = queues.keys()

    def on_data(self, dato):
        currenttime = datetime.now()
        diff = currenttime - Listener.inicio
        diffmin = diff.total_seconds()/60
        if diffmin<Listener.limit:
            try:
                for term in self.queues.keys():
                    str23=json.loads(dato)['text']
                    if term in str23:
                        self.queues[term].put(dato, False)
                #print("Recibo dato %s" % dato)
            except BaseException as e:
                pass
                #print("Error on_data: %s" % str(e))
        else:
            return False
    def on_error(self, status):
        print (status)

if __name__ == "__main__":
    vector = socket.recv_json()
    #print(vector)
    tiempo = vector[len(vector)-1]
    vector.pop()
    Listener.inicio = datetime.now()
    Listener.limit = float(tiempo)
    queues = {}

    for term in vector:
        queues[term] = Queue()
        Thread(target=Worker, args=(term, queues[term])).start()

    l = Listener(queues)
    stream = Stream(auth, l)
    stream.filter(track=vector)

    for term in vector:
        queues[term].put('0', False)
        name="%s.json"% str(term)
        open(name,'a')

    for term in vector:
        name="%s.json" % str(term)
        subir_a_Dropbox(name)
        os.remove(name)
    subir_a_Dropbox("Common.json")
    os.remove("Common.json")

    socket.send_json(vector)
