#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import sleep

btn = Button()
i = 0
while not btn.backspace and i < 10000:
    print(i)
    i += 1