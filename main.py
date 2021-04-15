#!/usr/bin/python
import sys
import os
import time
import keyboard
import evdev

from termios import tcflush, TCIOFLUSH
from pathlib import Path

#---- CLASSES ----

class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

#---- MAIN ----

if (len(sys.argv) != 2):	
	print("\nNo argument passed, terminating.\nNote that once configured, the argument" + bcolors.YELLOW + " \"run\"" + bcolors.RESET + " is required.\n")
	sys.exit(1)

mode = sys.argv[1]

if mode == "config":
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

elif mode == "run":	
	#run normally
	if not os.path.isfile("/etc/EasyKeyboardManager/config.txt"):
		sys.exit(2)

	cfg = open("/etc/EasyKeyboardManager/config.txt","r")
	data = cfg.readlines()

	main = data[0].replace("\n","").split(":=:")[1]
	macro = data[1].replace("\n","").split(":=:")[1]

	print("main = " + main)
	print("macro = " + macro)

	escapeSeq = False

	while(not escapeSeq):
		ev = keyboard.read_event(suppress=False)
		ev = keyboard.read_event(suppress=False)
		if ev.device == macro:
			#do something to revert the action and trigger the 
			keyboard.press_and_release("backspace")
			print("correct")

		#check exit contidition
	#	if not os.path.isfile(main) or not os.path.isfile(macro):
			#one of the keyboard is unplugged
	#		escapeSeq = True			

else:
	print("\nrunning mode argument passed is not correct.\nNote that the valid arguments are:" + bcolors.YELLOW + "\n\t\u00B7 config\n\t\u00B7 run\n" + bcolors.RESET)
	sys.exit(3)

	