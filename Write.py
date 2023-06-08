#!/usr/bin/env python

import RPi.GPIO as GPIO #to control the GPIO
from mfrc522 import SimpleMFRC522  #python library to read/write RFID tags via the budget MFRC522 RFID module

reader = SimpleMFRC522()

try:
	text = input('new data:')
	print("now place ur tag:")
	reader.write(text)  #this will write the desired text to the RFID tag
	print("written")
finally:
	GPIO.cleanup()
