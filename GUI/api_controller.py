import requests
import datetime
import controller as db_controller

IP = db_controller.getIP()
URL = f'http://{IP}:8017/api'

def convertDataTimeToLocal(dateTime):

    time = dateTime
    time = time[:-1]
    time = time[:time.index('T')] + ' ' + time[time.index('T')+1:]

    date = datetime.datetime.fromisoformat(time)
    
    return (date + datetime.timedelta(hours=7))


def getAllJunction():
    try:
        response = requests.get(URL+'/junctions')
        if response.status_code == 200:
            return response.json()
        else:
            return []
        
    except requests.exceptions.HTTPError as err:
        print('HTTPError')
        return []
    except requests.exceptions.Timeout:
        print("Timeout")
        return []
    # Maybe set up for a retry, or continue in a retry loop
    except requests.exceptions.TooManyRedirects:
        print('TooManyRedirects')
        return[]
        # Tell the user their URL was bad and try a different one
    except requests.exceptions.RequestException as e:
        print('RequestException')
        return []

def getFixtimeTabel(id):
    response = requests.get(URL+f'/fixtime_mode/byJunctionID/{id}')
    if response.status_code == 200:
        return response.json()
    else:
        return False

def getPlanByID(id):
    response = requests.get(URL+f'/plans/{id}')
    if response.status_code == 200:
        return response.json()
    else:
        return False
    
def getChannels(id):
    response = requests.get(URL+f'/channels/getByJunctionID/{id}')
    if response.status_code == 200:
        return response.json()
    else:
        return False
