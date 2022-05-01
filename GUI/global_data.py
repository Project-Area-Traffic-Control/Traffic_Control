import controller as db_controller
import socket_controller as socket

global current_phase
global temp_phase
global current_mode
global temp_mode
global current_plan_name
global timer
global phase_changed
global plans_data

global junction 
global channel

current_phase = 1
temp_phase = 1
current_mode = 'auto'
temp_mode = 'auto'
current_plan_name = 'เช้า'
timer = 120
phase_changed = True


def updateJunction():
    global junction 
    junction = db_controller.getJunction()
def updateChannel():
    global channel 
    channel = db_controller.getChannels()
def updatePlansData():
    global plans_data
    plans_data = db_controller.getPlans()

updateJunction()
updateChannel()
updatePlansData()

def updateCurrentPhase(newPhase):
    global current_phase
    global temp_phase
    socket.emitPhase(newPhase)
    temp_phase = current_phase
    current_phase = newPhase
def getCurrentPhase():
    global current_phase
    return current_phase

def updateCurrentMode(newMode):
    global current_mode
    global temp_mode
    socket.emitMode(newMode)
    temp_mode = current_mode
    current_mode = newMode
def getCurrentMode():
    global current_mode
    return current_mode

def updateCurrentPlanName(newplan):
    global current_plan_name
    current_plan_name = newplan
def getCurrentPlanName():
    global current_plan_name
    return current_plan_name

def updateTimer(newtime):
    global timer
    socket.emitTimer(newtime)
    timer = newtime
def getTimer():
    global timer
    return timer

