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


try:
    q = Queue(2)
    t1 = Worker(q,"T1")
    t2 = Worker(q,"T1")
    t1.start()
    t2.start()
    q.put(t1)
    q.put(t2)
    q.join()
except:
    print("ERROR")

print("holis")
