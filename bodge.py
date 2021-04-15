#!/usr/bin/python

import time
import keyboard

time.sleep(2)
print("ok")
while True:
	ev = keyboard.read_event(suppress=False)
	if(ev.device == "/dev/input/event24"):
		keyboard.write("red")
		#keyboard.press_and_release("backspace")