#!/usr/bin/env python
import time
#import board
import pyrebase
import random
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)  #red LED
GPIO.setup(23,GPIO.OUT)  #green LED
GPIO.setup(16,GPIO.IN)  #button
reader = SimpleMFRC522()

config = {
    "apiKey": "AIzaSyDBcOsMYrvOv5nb0GMszO_ZIYN7p-9fsKkQ",
    "authDomain": "iotca-project.firebaseapp.com",
    "databaseURL": "https://iotca-project-default-rtdb.firebaseio.com",
    "storageBucket": "iotca-project.appspot.com"
    }

firebase = pyrebase.initialize_app(config)

db = firebase.database()

while not GPIO.input(16):
	try:
		print("test")
		id, text = reader.read()  #read values from RFID tag 
		print(id)
		print(text)
		data = {
            "id" : id,
            "text": text
        }
		label, name = text.split(": ") # split the text into occupation and name
		label = label.strip()  #delete trailing or leading spaces 
		name = name.strip()
		#if the person is a professor, turn on the red LED for 3 seconds 
		if label == "Professor":
			GPIO.output(18,GPIO.HIGH)
			time.sleep(3)
			GPIO.output(18,GPIO.LOW)
		#if the person is a student, turn on the green LED for 3 seconds 
		elif label == "Student":
			GPIO.output(23,GPIO.HIGH)
			time.sleep(3)
			GPIO.output(23,GPIO.LOW)
		#if the person is a neither, turn on both LEDS for 3 seconds
		else:
			GPIO.output(23,GPIO.HIGH)
			GPIO.output(18,GPIO.HIGH)
			time.sleep(3)
			GPIO.output(18,GPIO.LOW)
			GPIO.output(23,GPIO.LOW)
		db.child("Status").push(data)
		db.update(data)
		print("sent to firebase")
	except RuntimeError as error:
		print(error.args[0])
		time.sleep(2.0)
		continue
	except Exception as error:
		GPIO.cleanup()
		raise error
		time.sleep(5)

