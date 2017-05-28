from threading import Thread
from queue import *

import zmq
import json

class Worker(Thread):
    def __init__(self, queue, name):
        self.queue=queue
        Thread.__init__(self, name=name)
    def run(self):
        # LO QUE HAGA EL WORKER
        self.queue.task_done()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:1024")

vector = socket.recv_json()
print(vector)

try:
    q = Queue(nThreads)
    for i in range(nThreads):
        t = Worker(q,"T"+str(i+1))
        t.start()
        q.put(t)
    q.join()
except:
    print("ERROR")
