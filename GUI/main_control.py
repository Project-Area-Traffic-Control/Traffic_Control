
from cmath import phase
import datetime
import threading
import time
import controller as db_controller
import global_data as GlobalData
import trafficLightController as Traffic_control

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
    state_Flashing = False

    while stop_thread:

        current_mode = GlobalData.current_mode
        current_phase = GlobalData.current_phase
        
        if temp_mode != current_mode:
            print('change mode to ',current_mode)

            if  current_mode == 'auto':
                if current_plan['name'] != 'ALLRED' and current_plan['name'] != 'FLASHING':
                    temp_auto = 'auto'
                    order = 1
                    if GlobalData.temp_mode == 'manual':
                        setYellow()
                        pattern = patterns[order-1]['pattern']
                        phase = pattern[8]
                        drivePhaseAuto(phase)
                        driveAuto(patterns[order-1]['pattern'])
                    
                    if GlobalData.temp_mode == 'red' or GlobalData.temp_mode == 'flashing':
                        drivePhaseAuto(current_phase)
                        
                    GlobalData.updateTimer(patterns[order-1]['duration'])

                else:
                    GlobalData.updateTimer(0)
                    driveAllRed()
                
                
            elif current_mode == 'manual':
                GlobalData.updateTimer(0)
                GlobalData.updateCurrentPhase(current_phase)
                drivePhase(current_phase)

            elif current_mode == 'red':
                GlobalData.updateTimer(0)
                if GlobalData.temp_mode == 'manual' or GlobalData.temp_mode == 'auto' :
                    if current_plan['name'] != 'ALLRED' and current_plan['name'] != 'FLASHING':
                        GlobalData.phase_changed = False
                        setYellow()
                        GlobalData.phase_changed = True
                driveAllRed()
            elif current_mode == 'flashing':
                GlobalData.updateTimer(0)
                if GlobalData.temp_mode == 'manual' or GlobalData.temp_mode == 'auto':
                    GlobalData.phase_changed = False
                    setYellow()
                    delayRed()
                    GlobalData.phase_changed = True

        
        if temp_phase != current_phase:
            print('change phase to ', current_phase)
            if current_mode == 'manual':
                drivePhaseManual(GlobalData.current_phase)
                GlobalData.updateTimer(0)
            elif current_mode == 'auto':
                if current_plan['name'] != 'ALLRED' and current_plan['name'] != 'FLASHING':
                    drivePhaseAuto(GlobalData.current_phase)
                 

        if current_mode == 'manual' or current_mode == 'auto':
            now = datetime.datetime.now()
            if now - datetime.timedelta(seconds=1) >= temp_now_1_sec: 
                temp_now_1_sec = datetime.datetime.now()

                if current_mode == 'manual':
                    t = GlobalData.timer
                    GlobalData.updateTimer(t+1)

                if current_mode == 'auto' and current_plan['name'] != 'ALLRED' and current_plan['name'] != 'FLASHING':
                    t = GlobalData.timer
                    GlobalData.updateTimer(t-1)

                    if GlobalData.timer <= 0:
                        
                        if temp_auto == 'auto':
                            setYellowPhase(GlobalData.current_phase)
                            GlobalData.updateTimer(current_plan['yellow_time'])
                            temp_auto = 'yellow'

                        elif temp_auto == 'yellow':
                            setAllRed()
                            GlobalData.updateTimer(current_plan['delay_red_time'])
                            temp_auto = 'red'

                        elif temp_auto == 'red':
                            order += 1
                            if order > len(patterns):
                                order = 1
                            driveAuto(patterns[order-1]['pattern'])
                            GlobalData.updateTimer(patterns[order-1]['duration'])
                            temp_auto = 'auto'

                        
                    
                
        if current_mode == 'flashing' or current_plan['name'] == 'FLASHING':
            now = datetime.datetime.now()
            if now - datetime.timedelta(milliseconds=500) >= temp_now_500_msec: 
                temp_now_500_msec = datetime.datetime.now()
                driveFlashing(state_Flashing)
                state_Flashing = not state_Flashing



        now = datetime.datetime.now()
        end = current_plan['end']
        now = datetime.datetime.now()
        t = now.replace(hour=0,minute=0,second=59,microsecond=999999)
        end = t + end

        if end.time() < datetime.datetime.now().time():
            print('Reload')
            reloadPattern()
          
            
        temp_mode = current_mode
        temp_phase = current_phase
        time.sleep(0.001)




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

def setAllRed():
    Traffic_control.setAllRed()
    print('All Red')