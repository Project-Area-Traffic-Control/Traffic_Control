import re
import socketio

sio = socketio.Client()

status_connect = False

@sio.event
def connect():
    global status_connect
    status_connect = True
    print("I'm connected!")

@sio.event
def connect_error(data):
    global status_connect
    status_connect = False
    print("The connection failed!")

@sio.event
def disconnect():
    global status_connect
    status_connect = False
    print("I'm disconnected!")



def connect(ip):
    try:
        sio.connect('http://'+ip+':8017/socket')
    except socketio.exceptions.ConnectionError as err:
        raise Exception("Connot connect to server.")

def disconnect():
    sio.disconnect()

def getStatus():
    return status_connect