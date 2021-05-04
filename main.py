#!/usr/bin/python
import sys
import os
import time
import keyboard

from evdev import InputDevice, categorize, ecodes
from termios import tcflush, TCIOFLUSH
from pathlib import Path

#---- CLASSES AND CONFIGURATIONS----

typing_speed = 0.01

class bcolors:
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	RESET = '\033[0m'

#---- CALLBACKS N FUNCTION----

def verify_system_integrity(device):
	if not os.path.exists(device):
		sys.exit(3)

def config():
	#execute configuration
	print(bcolors.GREEN + "\nInitializing configuration procedure .",end="",flush=True)
	#Fancy startup stuff. Prolly going to remove it
	time.sleep(0.5)
	print(".",end="", flush=True)
	time.sleep(0.5)
	print(".",flush=True)
	time.sleep(0.5)
	print(bcolors.RESET)

	#Create the folder for the configurations, if it it doesen't exist
	Path("/etc/EasyKeyboardManager/").mkdir(parents=True, exist_ok=True)
	outfile = open("/etc/EasyKeyboardManager/config.txt", "w")

	#actual configuration
	print("Press any key on your " + bcolors.YELLOW + "MAIN" + bcolors.RESET + " keyboard")
	ev = keyboard.read_event(suppress=False)
	#double to capture the press AND the release		
	ev = keyboard.read_event(suppress=False)		
	mainK = ev.device
	print("\nSaving " + bcolors.YELLOW + mainK + bcolors.RESET + " as MAIN keyboard")

	time.sleep(0.5)

	print("\n\nPress any key on your " + bcolors.RED + "MACRO" + bcolors.RESET + " keyboard")
	ev = keyboard.read_event(suppress=False)	
	#double to capture the press AND the release	
	ev = keyboard.read_event(suppress=False)		
	macroK = ev.device
	print("\nSaving " + bcolors.RED + macroK + bcolors.RESET + " as MACRO keyboard")

	#write the file
	outfile.write("MAIN:=:"+mainK+"\n")
	outfile.write("MACRO:=:"+macroK)

	outfile.close()
	print("\nConfig file saved in /etc/EasyKeyboardManager/config.txt" + bcolors.GREEN + "\nConfiguration procedure complete.\n" + bcolors.RESET)
	
	#Flush stdin to prompt a clear terminal
	time.sleep(0.5)
	tcflush(sys.stdin, TCIOFLUSH)

def run():
	if not os.path.isfile("/etc/EasyKeyboardManager/config.txt"):
		sys.exit(2)

	cfg = open("/etc/EasyKeyboardManager/config.txt","r")
	data = cfg.readlines()

	main = data[0].replace("\n","").split(":=:")[1]
	macro = data[1].replace("\n","").split(":=:")[1]

	print("main = " + main)
	print("macro = " + macro)

	verify_system_integrity(main)
	verify_system_integrity(macro)

	dev = InputDevice(macro)
	dev.grab()

	ctrl = False
	alt = False

	for event in dev.read_loop():
		verify_system_integrity(main)
		verify_system_integrity(macro)

		if event.type == ecodes.EV_KEY:
			key = categorize(event)
			
			if key.keystate == key.key_down and key.keycode == "KEY_LEFTCTRL":
				ctrl = True
			elif key.keystate == key.key_up and key.keycode == "KEY_LEFTCTRL":
				ctrl = False

			if key.keystate == key.key_down and key.keycode == "KEY_LEFTALT":
				alt = True
			elif key.keystate == key.key_up and key.keycode == "KEY_LEFTALT":
				alt = False

			if key.keystate == key.key_down:
				if key.keycode == 'KEY_DOT':
					if ctrl and alt:
						tcflush(sys.stdin, TCIOFLUSH)
						sys.exit(0)
				
				if key.keycode == 'KEY_H':
					keyboard.write("this is the official test",delay=typing_speed)
				
				if key.keycode == 'KEY_G':
					recorded = keyboard.record(until='enter')
					
					keyboard.write("git add .",delay=typing_speed)
					keyboard.press_and_release("enter")
					
					keyboard.write("git commit -m '",delay=typing_speed)
					keyboard.play(recorded[:-1],speed_factor=10.0)
					keyboard.press_and_release("'+enter")

					keyboard.write("git push origin master",delay=typing_speed)

					keyboard.press_and_release("enter")

#---- MAIN ----
if len(sys.argv) != 2:	
	print("\nNo argument passed, terminating.\nNote that once configured, the argument" + bcolors.YELLOW + " \"run\"" + bcolors.RESET + " is required.\n")
	sys.exit(1)

mode = sys.argv[1]

if mode == "config":
	config()
elif mode == "run":
	run()
else:
	print("\nrunning mode argument passed is not correct.\nNote that the valid arguments are:" + bcolors.YELLOW + "\n\t\u00B7 config\n\t\u00B7 run\n" + bcolors.RESET)
	sys.exit(3)