import time

import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)

mcp1 = MCP23017(i2c, address=0x21)
mcp2 = MCP23017(i2c, address=0x22)
mcp3 = MCP23017(i2c, address=0x23)


class PORT_SIGNAL:
    def __init__(self, red, green, yellow):
        self.red = red
        self.green = green
        self.yellow = yellow


port = []

for i in range(4):
    p = PORT_SIGNAL(mcp1.get_pin(i*3), mcp1.get_pin((i*3)+1),
                    mcp1.get_pin((i*3)+2))
    port.append(p)


p5 = PORT_SIGNAL(mcp1.get_pin(15), mcp2.get_pin(0),
                    mcp2.get_pin(1))

port.append(p5)


port[0].switch_to_output(value=True)

while True:
    for p in port:
        p.red.value = True
        p.green.value = True
        p.yellow.value = True
    
    time.sleep(0.5)
    for p in port:
        p.red.value = False
        p.green.value = False
        p.yellow.value = False
    
    time.sleep(0.5)
