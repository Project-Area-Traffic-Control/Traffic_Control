
from cmath import phase
import datetime
import time
import controller as db_controller
import global_data as GlobalData
import trafficLightController as Traffic_control


def loop():
    global stop_thread
    global current_plan
    global patterns
    global order
    global temp_auto
    stop_thread = True
    temp_auto = 'auto'
    order = 1
    temp_now_1_sec = datetime.datetime.now()
    temp_now_500_msec = datetime.datetime.now()
    
    current_plan = getCurrentPlan()
    patterns = db_controller.getPatternByPlanID(current_plan['plan_id'])
    GlobalData.updateCurrentPlanName(current_plan['name'])

    GlobalData.updateTimer(patterns[order-1]['duration'])
    
    phase = patterns[order-1]['pattern'][8]
    phase = int(phase)

    GlobalData.updateCurrentPhase(phase)
    

    print(patterns)

    temp_mode = -1
    temp_phase = -1
    state_Flashing = False

    while stop_thread:

        current_mode = GlobalData.current_mode
        current_phase = GlobalData.current_phase
        
        if temp_mode != current_mode:
            print('change mode to ',current_mode)
            if  current_mode == 'auto':
                temp_auto = 'auto'
                order = 1
                if GlobalData.temp_mode == 'manual':
                    setYellow()
                driveAuto(patterns[order-1]['pattern'])
                GlobalData.updateTimer(patterns[order-1]['duration'])
                
            elif current_mode == 'manual':
                GlobalData.updateTimer(0)
            elif current_mode == 'red':
                GlobalData.updateTimer(0)
                if GlobalData.temp_mode == 'manual' or GlobalData.temp_mode == 'auto':
                    setYellow()
                driveAllRed()
            elif current_mode == 'flashing':
                GlobalData.updateTimer(0)
                if GlobalData.temp_mode == 'manual' or GlobalData.temp_mode == 'auto':
                    setYellow()
        
        if temp_phase != current_phase:
            print('change phase to ', current_phase)
            if current_mode == 'manual':
                drivePhaseManual(GlobalData.current_phase)
                GlobalData.updateTimer(0)
            elif current_mode == 'auto':
                drivePhaseAuto(GlobalData.current_phase)
                 

        if current_mode == 'manual' or current_mode == 'auto':
            now = datetime.datetime.now()
            if now - datetime.timedelta(seconds=1) >= temp_now_1_sec: 
                temp_now_1_sec = datetime.datetime.now()

                if current_mode == 'manual':
                    t = GlobalData.timer
                    GlobalData.updateTimer(t+1)
                if current_mode == 'auto':
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

                        
                    
                
        if current_mode == 'flashing':
            now = datetime.datetime.now()
            if now - datetime.timedelta(milliseconds=500) >= temp_now_500_msec: 
                temp_now_500_msec = datetime.datetime.now()
                driveFlashing(state_Flashing)
                state_Flashing = not state_Flashing



        now = datetime.datetime.now()
        end = current_plan['end']
        now = datetime.datetime.now()
        t = now.replace(hour=0,minute=0,second=0,microsecond=0)
        end = t + end

        if end.time() < datetime.datetime.now().time():
            reloadPattern()
          


            
        temp_mode = current_mode
        temp_phase = current_phase
        time.sleep(0.001)


def stop():
    global stop_thread
    stop_thread = False

def reloadPattern():
    global current_plan
    global patterns
    current_plan = getCurrentPlan()
    patterns = db_controller.getPatternByPlanID(current_plan['plan_id'])
    GlobalData.updateCurrentPlanName(current_plan['name'])



def getCurrentPlan():
    data = db_controller.getPlans()
    for item in data:
        start = item['start']
        end = item['end']
        now = datetime.datetime.now()
        t = now.replace(hour=0,minute=0,second=0,microsecond=0)
        start = t + start
        end = t + end
        if start.time() < now.time() and now.time() < end.time():
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
    Traffic_control.setOffAll()
    if GlobalData.junction['number_channel'] == 3:
        if phase == 1:
            Traffic_control.setLightOn(channel[0]['port_right'],'g')
        elif phase == 2:
            Traffic_control.setLightOn(channel[1]['port_right'],'g')
            Traffic_control.setLightOn(channel[1]['port_foward'],'g')
        elif phase == 3:
            Traffic_control.setLightOn(channel[2]['port_foward'],'g')
            Traffic_control.setLightOn(channel[1]['port_foward'],'g')
        elif phase == 4:
            Traffic_control.setLightOn(channel[1]['port_right'],'g')




def setYellowPhase(phase):
    channel = GlobalData.channel
    Traffic_control.setOffAll()
    if GlobalData.junction['number_channel'] == 3:
        if phase == 1:
            Traffic_control.setLightOn(channel[0]['port_right'],'y')
        elif phase == 2:
            Traffic_control.setLightOn(channel[1]['port_right'],'y')
            Traffic_control.setLightOn(channel[1]['port_foward'],'y')
        elif phase == 3:
            Traffic_control.setLightOn(channel[2]['port_foward'],'y')
            Traffic_control.setLightOn(channel[1]['port_foward'],'y')
        elif phase == 4:
            Traffic_control.setLightOn(channel[1]['port_right'],'y')

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