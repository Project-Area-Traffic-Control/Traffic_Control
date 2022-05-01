import re
from socket import socket
import time
import socketio
import global_data as GlobalData
import controller as db_controller
import api_controller as api
import main_control as control

sio = socketio.Client()

global status_connect
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


@sio.on('update:setting')
def on_message(data):
    junctionID = GlobalData.junction['id']
    print(data['junction_id'],junctionID)
    if str(data['junction_id']) == str(junctionID):
        status = loadDataToDB()
        print('reload')
        if status:
            control.stop()
            control.runThreading()

@sio.on('get:data')
def on_message(data):
    
    junctionID = GlobalData.junction['id']
    if str(data) == str(junctionID):
        print(data)
        sio.emit('update:data',{'junction_id' : GlobalData.junction['id'], 'phase': GlobalData.current_phase , 'mode': GlobalData.current_mode , 'Timer': GlobalData.timer})



def connect(ip):
    try:
        sio.connect('http://'+ip+':8017/socket')
    except socketio.exceptions.ConnectionError as err:
        raise Exception("Connot connect to server.")

def disconnect():
    sio.disconnect()
    

def getStatus():
    global status_connect
    return status_connect


def emitPhase(phase):
    global status_connect
    if status_connect:
        print('Emit',phase)
        sio.emit('update:phase',{'junction_id' : GlobalData.junction['id'], 'phase': phase})
def emitMode(mode):
    if status_connect:
        sio.emit('update:mode',{'junction_id' : GlobalData.junction['id'], 'mode': mode})
def emitTimer(timer):
    if status_connect:
        sio.emit('update:timer',{'junction_id' : GlobalData.junction['id'], 'timer': timer})

















def loadDataToDB():
    junctionData = db_controller.getJunction()
    result = api.getFixtimeTabel(junctionData['id'])
    if result:
        db_controller.deleteAllPlan()
        db_controller.deleteAllPattern()
        n = 0
        for item in result:
            start = api.convertDataTimeToLocal(item['start'])
            end = api.convertDataTimeToLocal(item['end'])
            data = {
                'id': n,
                'start': start.time().replace(second=0),
                'end': end.time().replace(second=0),
                'name': item['plan']['name'],
                'yellow_time': item['plan']['yellow_time'],
                'delay_red_time': item['plan']['delay_red_time'],
                'plan_id': item['plan']['id'],
            }
            db_controller.addPlan(data)

            patterns = api.getPlanByID(data['plan_id'])['pattern']
            for pattern in patterns:
                dataPattern = {
                    "plan_id": n,
                    "pattern": pattern['pattern'],
                    "order": pattern['order'],
                    "duration": pattern['duration']
                }
                db_controller.addPattern(dataPattern)

            n += 1

        
        loadChanelToDB()
        loadJunctionDataToDB()
        updateDataPlans()

        time.sleep(0.2)
        loadDataToGlobal()

        return True
    else:
        return False

def updateDataPlans():
    GlobalData.plans_data = db_controller.getPlans()

def loadChanelToDB():
        junctionData = GlobalData.junction
        result = api.getChannels(junctionData['id'])
        db_controller.deleteAllChannel()
        for item in result:
            global port_forward
            global port_right
            port_forward = 0
            port_right = 0

            for phase in item['phase']:
     

                if phase['type'] == 'FORWARD':
                    port_forward = phase['port_number']
                elif phase['type'] == 'TURN_RIGHT':
                    port_right = phase['port_number']

            data = {
                "order_number": item['order'],
                "name":  item['name'],
                "port_forward": port_forward,
                "port_right": port_right
            }
            db_controller.addChannel(data)

def loadDataToGlobal():
        GlobalData.updateJunction()
        GlobalData.updateChannel()
        GlobalData.updatePlansData()

def loadJunctionDataToDB():
        new_junction = api.getJunctionByID(GlobalData.junction['id'])
        data  = {
            'id': new_junction['id'],
            'name': new_junction['name'],
            'number_channel': new_junction['number_channel'],
            'rotate': new_junction['rotate']
        }
        print(data)
        db_controller.updateJunction(data)