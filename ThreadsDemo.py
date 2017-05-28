from threading import Thread
from queue import *

#Declaración de una tarea
class Worker(Thread):
    def __init__(self, queue, name):
        self.queue=queue
        Thread.__init__(self, name=name)
    def run(self):
        for i in range(3):
            print(str(i+1)+"--"+self.getName())
        self.queue.task_done()


nThreads = 20
try:
    q = Queue(nThreads)
    for i in range(nThreads):
        t = Worker(q,"T"+str(i+1))
        t.start()
        q.put(t)
    q.join()
except:
    print("ERROR")

print("holis")
