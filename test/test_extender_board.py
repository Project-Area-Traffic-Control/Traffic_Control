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

for i in range(15):

    p = PORT_SIGNAL(mcp1.get_pin(i*3), mcp1.get_pin((i*3)+1),
                    mcp1.get_pin((i*3)+2))
    port.append(p)


PA1_R = mcp1.get_pin(0)
PA1_G = mcp1.get_pin(1)
PA1_Y = mcp1.get_pin(2)

PA2_R = mcp1.get_pin(3)
PA2_G = mcp1.get_pin(4)
PA2_Y = mcp1.get_pin(5)

PA3_R = mcp1.get_pin(6)
PA3_G = mcp1.get_pin(7)
PA3_Y = mcp1.get_pin(8)

PA4_R = mcp1.get_pin(9)
PA4_G = mcp1.get_pin(10)
PA4_Y = mcp1.get_pin(11)

PA5_R = mcp1.get_pin(12)
PA5_G = mcp1.get_pin(13)
PA5_Y = mcp1.get_pin(14)

pin0.switch_to_output(value=True)


while True:
    pin0.value = True
    time.sleep(0.5)
    pin0.value = False
    time.sleep(0.5)
