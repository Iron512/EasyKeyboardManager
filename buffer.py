#!/usr/bin/python
import sys
import os
import time
import keyboard

from evdev import InputDevice, categorize, ecodes

ev = keyboard.read_event(suppress=False)	
ev = keyboard.read_event(suppress=False)

dev = InputDevice(ev.device)
main = InputDevice(ev.device)

print("ok")

for event in dev.read_loop():
	if event.type == ecodes.EV_KEY:
		key = categorize(event)
			
		if key.keystate == key.key_down and key.keycode == "KEY_G":
			print("hail")
			#Trigger buffer reading
			mstr = ""
			for event in dev.read_loop():
				if event.type == ecodes.EV_KEY:
					key = categorize(event)

					if key.keystate == key.key_down and key.keycode == "KEY_ENTER":
						print(mstr.lower())
						break
					elif key.keystate == key.key_down:
						mstr += str(key.keycode.replace("KEY_",""))