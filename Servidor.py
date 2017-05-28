import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:1024")

hashgt = socket.recv_json()
print(hashgt)
