import datetime
import time
import controller as db_controller
import socket_controller as socket


global current_phase
global current_plan
global temp_phase
global current_mode
global temp_mode
global current_plan_name
global timer
global phase_changed
global plans_data
global ip_server

global junction 
global channel

current_phase = 1
temp_phase = 1
current_mode = 'auto'
temp_mode = -1
current_plan_name = 'เช้า'
timer = 120
phase_changed = True


def updateJunction():
    global junction 
    global ip_server
    time.sleep(0.01)
    junction = db_controller.getJunction()
    time.sleep(0.01)
    ip_server = db_controller.getIP()
def updateChannel():
    global channel 
    time.sleep(0.01)
    channel = db_controller.getChannels()
def updatePlansData():
    global plans_data
    time.sleep(0.01)
    data = db_controller.getPlans()
    plans_data = data



updateJunction()
updateChannel()
updatePlansData()


def updateCurrentPlan(plan):
    global current_plan
    current_plan = plan

def updatePhase_changed(data):
    global phase_changed
    phase_changed = data

def updateCurrentPhase(newPhase):
    global current_phase
    global temp_phase
    temp_phase = current_phase
    current_phase = newPhase

def updateCurrentMode(newMode):
    global current_mode
    global temp_mode
    # socket.emitMode(newMode)
    # temp_mode = current_mode
    current_mode = newMode

def updateTemp_mode(temp):
    global temp_mode
    temp_mode = temp

def updateCurrentPlanName(newplan):
    global current_plan_name
    current_plan_name = newplan

def updateTimer(newtime):
    global timer
    socket.emitTimer(newtime)
    timer = newtime



def updateCurrentPlanFromDB():

    data = db_controller.getPlans()
    for item in data:
        start = item['start']
        end = item['end']
        now = datetime.datetime.now()
        t1 = now.replace(hour=0,minute=0,second=0,microsecond=0)
        t2 = now.replace(hour=0,minute=0,second=59,microsecond=999999)
        start = t1 + start
        end = t2 + end
        # print(start.time(),now.time(),end.time())
        if start.time() <= now.time() and now.time() <= end.time():
            updateCurrentPlan(item)