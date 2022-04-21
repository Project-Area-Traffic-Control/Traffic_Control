import socketio

sio = socketio.Client()

junction_id = 5
check_loop = True
check_input = False
input_state = 0
isAutomode = True


@sio.event
def connect():
    print('connection established : ', sio.sid)


@sio.on('setPhase'+str(junction_id))
def on_message(data):
    # print('I received a message!', data)

    global input_state
    global check_input
    global isAutomode

    if isAutomode == False:
        phase = data["phase"]
        input_state = phase

        print("Set phase form server : ",phase)

        check_input = True


@sio.on('setMode'+str(junction_id))
def on_message(data):
    # print('I received a message!', data)
    
    global input_state
    global check_input
    global isAutomode

    print("Set mode form server : ",end='')

    mode = data["mode"]

    if mode == 0:
        input_state = 9
        print("Auto mode")
        isAutomode = True
    elif mode == 1:
        print("Manual mode")
        input_state = 0
        isAutomode = False

    check_input = True


sio.connect('http://localhost:3000')