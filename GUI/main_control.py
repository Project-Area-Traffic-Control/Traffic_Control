import datetime
import threading
import time
import controller as db_controller
import global_data as GlobalData
import socket_controller as socket
import trafficLightController as Traffic_control


def runThreading():
    global thread
    thread = threading.Thread(target=loop)
    thread.start()
    print('start main control')

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
    global delay_yellow
    global delay_red
    global temp_plan_id
    global order
    global plan_name

    plan_name = 'Test'
    temp_plan_id = -1
    delay_red = 1
    delay_yellow = 3
    order = 1
    stop_thread = True
    temp_phase = -1
    state_flashing = False
    GlobalData.updateTemp_mode('Test')

    getCurrentPlan()

    while stop_thread:

        while GlobalData.current_mode == 'auto' and stop_thread:

            if plan_name == 'ALLRED' or plan_name == 'FLASHING':
                if GlobalData.temp_mode != GlobalData.current_mode:
                    print('change mode to auto')
                    if GlobalData.temp_mode == 'manual':
                        setYellowPhase(GlobalData.current_phase)
                        time.sleep(delay_yellow)
                    GlobalData.updateTemp_mode('auto')

                    GlobalData.updateTimer(0)

                if plan_name == 'ALLRED':
                    driveAllRed()    
                elif plan_name == 'FLASHING':
                    driveFlashing(state_flashing)
                    state_flashing = not state_flashing

                now = datetime.datetime.now()
                end = GlobalData.current_plan['end']
                t2 = now.replace(hour=0,minute=0,second=59,microsecond=999999)
                end = t2 + end
                if now.time() > end.time():
                    getCurrentPlan()

                    order = 1
                    patterns = getPatterns()
                    phase = getPhaseFromPattern(patterns[order-1]['pattern'])
                    GlobalData.updateTimer(patterns[order-1]['duration'])

                    GlobalData.updateCurrentPhase(phase)
                    GlobalData.phase_changed = True
                    drivePhase(phase)

            else:
                t = GlobalData.timer
                GlobalData.updateTimer(t-1)

                if GlobalData.temp_mode != GlobalData.current_mode:
                    print('change mode to auto')
                    if GlobalData.temp_mode == 'manual':
                        setYellowPhase(GlobalData.current_phase)
                        time.sleep(delay_yellow)
                    GlobalData.updateTemp_mode('auto')

                    order = 1
                    patterns = getPatterns()
                    phase = getPhaseFromPattern(patterns[order-1]['pattern'])
                    GlobalData.updateTimer(patterns[order-1]['duration'])

                    GlobalData.updateCurrentPhase(phase)
                    GlobalData.phase_changed = True
                    drivePhase(phase)

                if GlobalData.timer <= 0:
                    order += 1
                    patterns = getPatterns()
                    if plan_name == 'ALLRED' or plan_name == 'FLASHING':
                        continue
                    if order > len(patterns):
                        order = 1
                    phase = getPhaseFromPattern(patterns[order-1]['pattern'])

                    GlobalData.phase_changed = False
                    setYellowPhase(GlobalData.current_phase)
                    timerYellow = delay_yellow
                    GlobalData.updateTimer(timerYellow)
                    while timerYellow >= 0:
                        GlobalData.updateTimer(timerYellow)
                        timerYellow -= 1
                        time.sleep(1)
                    driveAllRed()
                    time.sleep(delay_red)

                    GlobalData.updateCurrentPhase(phase)
                    GlobalData.phase_changed = True
                    
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
                GlobalData.phase_changed = True
                drivePhase(current_phase)
                temp_phase = current_phase

            if temp_phase != current_phase:
                print('change phase from ',temp_phase, ' to ' , GlobalData.current_phase)
                GlobalData.phase_changed = False
                setYellowPhase(temp_phase)
                time.sleep(delay_yellow)
                
                GlobalData.updateTimer(0)
                GlobalData.updateCurrentPhase(current_phase)
                GlobalData.phase_changed = True
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
                time.sleep(delay_yellow)
                GlobalData.phase_changed = True
                
            driveAllRed()
            GlobalData.updateTemp_mode('red')
        
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
    global delay_yellow
    global delay_red
    global temp_plan_id
    global order
    global plan_name

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
            delay_yellow = int(item['yellow_time'])
            delay_red = int(item['delay_red_time'])
            if item['id'] != temp_plan_id:
                temp_plan_id = item['id']  
                order = 1

            plan_name = item['name']
            GlobalData.updateCurrentPlanName(plan_name)    
            GlobalData.updateCurrentPlan(item)
            return item

def drivePhase(phase):
    print('Drive phase : ',phase)
    channel = GlobalData.channel
    socket.emitPhase(phase)
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
            Traffic_control.setLightOnList([channel[0]['port_right'],channel[2]['port_foward']],'g')
        elif phase == 6:
            Traffic_control.setLightOnList([channel[1]['port_foward'],channel[3]['port_foward']],'g')
        elif phase == 7:
            Traffic_control.setLightOnList([channel[0]['port_foward'],channel[2]['port_right']],'g')
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
            Traffic_control.setLightOnList([channel[0]['port_right'],channel[2]['port_foward']],'y')
        elif phase == 6:
            Traffic_control.setLightOnList([channel[1]['port_foward'],channel[3]['port_foward']],'y')
        elif phase == 7:
            Traffic_control.setLightOnList([channel[0]['port_foward'],channel[2]['port_right']],'y')
        elif phase == 8:
            Traffic_control.setLightOnList([channel[1]['port_right'],channel[3]['port_right']],'y')

def driveAllRed():
    print('All Red')
    Traffic_control.setAllRed()

def driveFlashing(state):
    print('Flashing ',state)
    Traffic_control.setAllYellow(state)



