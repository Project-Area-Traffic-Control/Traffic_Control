import controller as db_controller
global current_phase
global temp_phase
global current_mode
global temp_mode
global current_plan_name
global timer
global phase_changed
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

updateJunction()
updateChannel()


def updateCurrentPhase(newPhase):
    global current_phase
    global temp_phase
    temp_phase = current_phase
    current_phase = newPhase
def getCurrentPhase():
    global current_phase
    return current_phase

def updateCurrentMode(newMode):
    global current_mode
    global temp_mode
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
    timer = newtime
def getTimer():
    global timer
    return timer

