import time
from tkinter import E

import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)

mcp1 = MCP23017(i2c, address=0x20)
mcp2 = MCP23017(i2c, address=0x21)
# mcp3 = MCP23017(i2c, address=0x01)


class PORT_SIGNAL:
    def __init__(self, red, green, yellow):
        self.red = red
        self.green = green
        self.yellow = yellow

        self.red.direction = digitalio.Direction.OUTPUT
        self.green.direction = digitalio.Direction.OUTPUT
        self.yellow.direction = digitalio.Direction.OUTPUT
    
    def setRed(self,value):
        self.red.value = value
    def setGreen(self,value):
        self.green.value = value
    def setYellow(self,value):
        self.yellow.value = value
    
    def setOffAll(self):
        self.red.value = False
        self.green.value = False
        self.yellow.value = False
    
p1 = PORT_SIGNAL(mcp1.get_pin(0),mcp1.get_pin(1),mcp1.get_pin(2))
p2 = PORT_SIGNAL(mcp1.get_pin(3),mcp1.get_pin(4),mcp1.get_pin(5))
p3 = PORT_SIGNAL(mcp1.get_pin(6),mcp1.get_pin(7),mcp1.get_pin(8))
p4 = PORT_SIGNAL(mcp1.get_pin(9),mcp1.get_pin(10),mcp1.get_pin(11))
p5 = PORT_SIGNAL(mcp1.get_pin(12),mcp1.get_pin(13),mcp1.get_pin(14))
p6 = PORT_SIGNAL(mcp1.get_pin(15),mcp2.get_pin(0),mcp2.get_pin(1))
p7 = PORT_SIGNAL(mcp2.get_pin(2),mcp2.get_pin(3),mcp2.get_pin(4))
p8 = PORT_SIGNAL(mcp2.get_pin(5),mcp2.get_pin(6),mcp2.get_pin(7))
p9 = PORT_SIGNAL(mcp2.get_pin(8),mcp2.get_pin(9),mcp2.get_pin(10))
p10 = PORT_SIGNAL(mcp2.get_pin(11),mcp2.get_pin(12),mcp2.get_pin(13))
# p11 = PORT_SIGNAL(mcp2.get_pin(14),mcp2.get_pin(15),mcp3.get_pin(0))
# p12 = PORT_SIGNAL(mcp3.get_pin(1),mcp3.get_pin(2),mcp3.get_pin(3))
# p13 = PORT_SIGNAL(mcp3.get_pin(4),mcp3.get_pin(5),mcp3.get_pin(6))
# p14 = PORT_SIGNAL(mcp3.get_pin(7),mcp3.get_pin(8),mcp3.get_pin(9))
# p15 = PORT_SIGNAL(mcp3.get_pin(10),mcp3.get_pin(11),mcp3.get_pin(12))
# p16 = PORT_SIGNAL(mcp3.get_pin(13),mcp3.get_pin(14),mcp3.get_pin(15))

p1.setRed(True)
PortSignel = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]

def setLightOn(portNumber,light):

    if(light == 'r'):
        PortSignel[portNumber-1].setRed(True)
        PortSignel[portNumber-1].setGreen(False)
        PortSignel[portNumber-1].setYellow(False)

    elif(light == 'g'):
        PortSignel[portNumber-1].setRed(False)
        PortSignel[portNumber-1].setGreen(True)
        PortSignel[portNumber-1].setYellow(False)
    
    elif(light == 'y'):
        PortSignel[portNumber-1].setRed(False)
        PortSignel[portNumber-1].setGreen(False)
        PortSignel[portNumber-1].setYellow(True)

def setOffAll():
    for port in PortSignel:
        port.setOffAll()
        
def setAllRed():
    for port in PortSignel:
        port.setRed(True)

setOffAll()
# setLightOn(1,'g')
# setLightOn(2,'g')
# setLightOn(4,'r')
# setLightOn(7,'r')
# setLightOn(8,'r') 
# port[0].switch_to_output(value=True)

# while True:
#     for p in port:
#         p.red.value = True
#         p.green.value = True
#         p.yellow.value = True
    
#     time.sleep(0.5)
#     for p in port:
#         p.red.value = False
#         p.green.value = False
#         p.yellow.value = False
    
#     time.sleep(0.5)
