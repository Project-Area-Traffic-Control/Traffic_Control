
from cmath import phase
import datetime
import threading
import time
import controller as db_controller
import global_data as GlobalData
# import trafficLightController as Traffic_control

def runThreading():
    global thread
    thread = threading.Thread(target=loop)
    thread.start()

def start():
    global thread
    thread.start()

def stop():
    global stop_thread
    stop_thread = False

    thread.join()

    print('stop')

def loop():
    global stop_thread
    global current_plan
    global patterns
    global order
    global temp_auto
    stop_thread = True
    temp_auto = 'auto'
    current_plan = False
    
    temp_now_1_sec = datetime.datetime.now()
    temp_now_500_msec = datetime.datetime.now()
    
    reloadPattern()

    order = 1

    if current_plan['name'] != 'FLASHING' and current_plan['name'] != 'ALLRED':
        GlobalData.updateTimer(patterns[order-1]['duration'])
        phase = patterns[order-1]['pattern'][8]
        phase = int(phase)
        GlobalData.updateCurrentPhase(phase)
    
    temp_mode = -1
    temp_phase = -1
    state_flashing = False


    while stop_thread:

        current_mode = GlobalData.current_mode
        current_phase = GlobalData.current_phase

        while GlobalData.current_mode == 'auto' and stop_thread:

            t = GlobalData.timer
            GlobalData.updateTimer(t-1)

            if GlobalData.temp_mode != GlobalData.current_mode:
                print('change mode to auto')
                GlobalData.updateTemp_mode('auto')

                order = 1
                patterns = getPatterns()
                phase = getPhaseFromPattern(patterns[order-1]['pattern'])
                GlobalData.updateTimer(patterns[order-1]['duration'])

                GlobalData.updateCurrentPhase(phase)
                drivePhase(phase)

            if GlobalData.timer <= 0:
                order += 1
                patterns = getPatterns()
                if order > len(patterns):
                    order = 1
                phase = getPhaseFromPattern(patterns[order-1]['pattern'])

                GlobalData.phase_changed = False
                setYellowPhase(GlobalData.current_phase)
                timerYellow = current_plan['yellow_time']
                GlobalData.updateTimer(timerYellow)
                while timerYellow > 0:
                    GlobalData.updateTimer(timerYellow)
                    timerYellow -= 1
                    time.sleep(1)
                GlobalData.phase_changed = True

                GlobalData.updateCurrentPhase(phase)
                GlobalData.updateTimer(patterns[order-1]['duration'])
                drivePhase(phase)

            
            time.sleep(1)

        while GlobalData.current_mode == 'manual' and stop_thread:
            current_phase = GlobalData.current_phase

            t = GlobalData.timer
            GlobalData.updateTimer(t+1)

            if GlobalData.temp_mode != GlobalData.current_mode:
                print('change mode to manual')
                GlobalData.updateTemp_mode('manual')
                
                GlobalData.updateTimer(0)
                GlobalData.updateCurrentPhase(current_phase)
                drivePhase(current_phase)

            if temp_phase != current_phase:
                print('change phase from ',temp_phase, ' to ' , GlobalData.current_phase)
                GlobalData.phase_changed = False
                setYellowPhase(temp_phase)
                time.sleep(current_plan['yellow_time'])
                GlobalData.phase_changed = True

                GlobalData.updateTimer(0)
                GlobalData.updateCurrentPhase(current_phase)
                drivePhase(current_phase)

            temp_phase = current_phase
          
            time.sleep(1)

        while GlobalData.current_mode == 'flashing' and stop_thread:
            
            if GlobalData.temp_mode != GlobalData.current_mode:
                print('change mode to flashing')
                GlobalData.updateTemp_mode('flashing')
                GlobalData.updateTimer(0)

            driveFlashing(state_flashing)
            state_flashing = not state_flashing
            time.sleep(1)
        
        if GlobalData.current_mode == 'red' and (GlobalData.temp_mode != GlobalData.current_mode):
            print('change mode to red')
            GlobalData.updateTimer(0)
            if GlobalData.temp_mode == 'manual' or GlobalData.temp_mode == 'auto':
                GlobalData.phase_changed = False
                setYellowPhase(GlobalData.current_phase)
                time.sleep(current_plan['yellow_time'])
                GlobalData.phase_changed = True
                
            driveAllRed()
            GlobalData.updateTemp_mode('red')
        
    


        temp_mode = current_mode
        temp_phase = current_phase

        time.sleep(0.001)


def getPatterns():
    plan = getCurrentPlan()
    return db_controller.getPatternByPlanID(plan['id'])

def getPattern(order):
    plan = getCurrentPlan()
    patterns = db_controller.getPatternByPlanID(plan['id'])
    return patterns[order-1]['pattern']

def getPhaseFromPattern(pattern):
    phase = pattern[8]
    return int(phase)

def getCurrentPlan():
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
            return item

def reloadPattern():
    global current_plan
    global patterns
    global order 

    if current_plan:
        if current_plan['name'] != 'ALLRED' and current_plan['name'] != 'FLASHING':
            stop()
            runThreading()

    current_plan = getCurrentPlan()
    # print(current_plan['name'])
    patterns = db_controller.getPatternByPlanID(current_plan['id'])
    GlobalData.updateCurrentPlanName(current_plan['name'])

    order = 0



def driveAuto(pattern):
    phase = pattern[8]
    phase = int(phase)
    GlobalData.updateCurrentPhase(phase)
    GlobalData.temp_phase = GlobalData.current_phase
     
def drivePhaseAuto(phase):
    drivePhase(phase)
    
def drivePhaseManual(phase):
    
    setYellow()
    delayRed()
    GlobalData.phase_changed = True
    GlobalData.temp_phase = GlobalData.current_phase
    drivePhase(phase)
    

def drivePhase(phase):
    print('Drive phase : ',phase)
    channel = GlobalData.channel
    if GlobalData.junction['number_channel'] == 3:
        if phase == 1:
            Traffic_control.setLightOnList([channel[0]['port_right']],'g')
        elif phase == 2:
            Traffic_control.setLightOnList([channel[1]['port_right'],channel[1]['port_foward']],'g')
        elif phase == 3:
            Traffic_control.setLightOnList([channel[2]['port_foward'],channel[1]['port_foward']],'g')
        elif phase == 4:
            Traffic_control.setLightOnList([channel[1]['port_right']],'g')

    elif GlobalData.junction['number_channel'] == 4:
        if phase == 1:
            Traffic_control.setLightOnList([channel[0]['port_right'],channel[0]['port_foward']],'g')
        elif phase == 2:
            Traffic_control.setLightOnList([channel[1]['port_right'],channel[1]['port_foward']],'g')
        elif phase == 3:
            Traffic_control.setLightOnList([channel[2]['port_right'],channel[2]['port_foward']],'g')
        elif phase == 4:
            Traffic_control.setLightOnList([channel[3]['port_right'],channel[3]['port_foward']],'g')
        elif phase == 5:
            Traffic_control.setLightOnList([channel[0]['port_foward'],channel[2]['port_foward']],'g')
        elif phase == 6:
            Traffic_control.setLightOnList([channel[1]['port_foward'],channel[3]['port_foward']],'g')
        elif phase == 7:
            Traffic_control.setLightOnList([channel[0]['port_right'],channel[2]['port_right']],'g')
        elif phase == 8:
            Traffic_control.setLightOnList([channel[1]['port_right'],channel[3]['port_right']],'g')


def setYellowPhase(phase):
    print('Set Yellow : ',phase)
    channel = GlobalData.channel
    if GlobalData.junction['number_channel'] == 3:
        if phase == 1:
            Traffic_control.setLightOnList([channel[0]['port_right']],'y')
        elif phase == 2:
            Traffic_control.setLightOnList([channel[1]['port_right'],channel[1]['port_foward']],'y')
        elif phase == 3:
            Traffic_control.setLightOnList([channel[2]['port_foward'],channel[1]['port_foward']],'y')
        elif phase == 4:
            Traffic_control.setLightOnList([channel[1]['port_right']],'y')

    elif GlobalData.junction['number_channel'] == 4:
        if phase == 1:
            Traffic_control.setLightOnList([channel[0]['port_right'],channel[0]['port_foward']],'y')
        elif phase == 2:
            Traffic_control.setLightOnList([channel[1]['port_right'],channel[1]['port_foward']],'y')
        elif phase == 3:
            Traffic_control.setLightOnList([channel[2]['port_right'],channel[2]['port_foward']],'y')
        elif phase == 4:
            Traffic_control.setLightOnList([channel[3]['port_right'],channel[3]['port_foward']],'y')
        elif phase == 5:
            Traffic_control.setLightOnList([channel[0]['port_foward'],channel[2]['port_foward']],'y')
        elif phase == 6:
            Traffic_control.setLightOnList([channel[1]['port_foward'],channel[3]['port_foward']],'y')
        elif phase == 7:
            Traffic_control.setLightOnList([channel[0]['port_right'],channel[2]['port_right']],'y')
        elif phase == 8:
            Traffic_control.setLightOnList([channel[1]['port_right'],channel[3]['port_right']],'y')

def driveAllRed():
    print('All Red')
    Traffic_control.setAllRed()

def driveFlashing(state):
    print('Flashing ',state)
    Traffic_control.setAllYellow(state)

def setYellow():
    global current_plan
    setYellowPhase(GlobalData.temp_phase)
    time.sleep(current_plan['yellow_time'])

def delayRed():
    global current_plan
    print("Red ")
    setAllRed()
    time.sleep(current_plan['delay_red_time'])
