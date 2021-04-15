#!/usr/bin/python
import sys
import usb.core #from pyusb

from pathlib import Path

class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

if (len(sys.argv) != 2):	
	print("\nNo argument passed, terminating.\nNote that once configured, the argument" + bcolors.YELLOW + " \"run\"" + bcolors.RESET + " is required.\n")
	sys.exit(1)

mode = sys.argv[1]

if mode == "config":
	#execute configuration
	print(bcolors.GREEN + "\nInitializing configuration procedure ...\n" + bcolors.RESET)
	print("These are the available USB devices. Pick your MAIN keyboard(s):\n")

	dev = usb.core.find(find_all=True)
	# loop through devices, printing vendor and product ids in decimal and hex

	counter = 1
	pairs = []

	for cfg in dev:
		manufacturer = usb.util.get_string(cfg, cfg.iManufacturer)
		product = usb.util.get_string(cfg, cfg.iProduct)
		print(str(counter) + ") - " + str(manufacturer) + " " + str(product))
		print("\tVID:{:04x}".format(cfg.idVendor) + " PID:{:04x}".format(cfg.idProduct))
		pairs.append((cfg.idVendor, cfg.idProduct))
		counter += 1

	print()
	secondaryK = []

	Path("/etc/EasyKeyboardManager/").mkdir(parents=True, exist_ok=True)
	outfile = open("/etc/EasyKeyboardManager/config.txt", "w")

	while(len(secondaryK) == 0):
		res = input()
		res = res.split(" ")

		for el in res:
			if el.isnumeric() and int(el) > 0 and int(el) < counter:
				secondaryK.append(pairs[int(el)-1])

	for item in secondaryK:
		outfile.write("{:04x}".format(item[0]) + ":=:{:04x}".format(item[1]))

	outfile.close()
	print("\nConfig file saved in /etc/EasyKeyboardManager/config.txt" + bcolors.GREEN + "\nconfiguration procedure complete.\n" + bcolors.RESET)

elif mode == "run":
	#run normally
	print("ok")
else:
	print("\nrunning mode argument passed is not correct.\nNote that the valid arguments are:" + bcolors.YELLOW + "\n\t\u00B7 config\n\t\u00B7 run\n" + bcolors.RESET)
	sys.exit(2)
