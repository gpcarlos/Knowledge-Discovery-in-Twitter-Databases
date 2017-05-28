import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:1024")

hashgt = ["PiratasDelCaribe","Alien","BladeRunner"]

socket.send_json(hashgt)
