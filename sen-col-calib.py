#!/usr/bin/env python3
# So program can be run from Brickman

from ev3dev.ev3 import *
from time import sleep


ts = TouchSensor()
cl = ColorSensor()
assert cl.connected, "Connect a color sensor to any sensor port"
cl.mode = 'COL-REFLECT'

def measure_color(say_prompt):
    Sound.speak(say_prompt).wait()
    color = cl.value()
    while not ts.value():
        color = cl.value()
    return color 
white = measure_color('Show me white')
print(white)
black = measure_color('Show me black')
print(black)

# white = cl.value()
# Sound.speak('Show me white').wait()
# while not ts.value():
#     white = cl.value()
# print(white)

# black = cl.value()
# Sound.speak('Show me black').wait()
# while not ts.value():
#     black = cl.value()
# print(black)
