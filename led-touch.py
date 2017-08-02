#!/usr/bin/env python3 
# from ev3dev.ev3 import *

import ev3dev.ev3 as ev3

print("jedeme")
ts = ev3.TouchSensor()
while True:
    ev3.Leds.set_color(ev3.Leds.LEFT, (ev3.Leds.GREEN, ev3.Leds.RED)[ts.value()])

# do not delete lines below
# export PATH=/usr/bin/python3:$PATH
# https://winsmarts.com/new-line-characters-in-text-files-between-mac-and-windows-3695b7beb685
# perl -pi -e 's/\r\n|\n|\r/\n/g'   file-to-convert