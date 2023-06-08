#!/usr/bin/env python
import time
import datetime
import requests
#import board
import pyrebase
import random
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(16,GPIO.IN)
reader = SimpleMFRC522()

config = {
    "apiKey": "AIzaSyDBcOsMYrvOv5nb0GMszO_ZIYN7p-9fsKkQ",
    "authDomain": "iotca-project.firebaseapp.com",
    "databaseURL": "https://iotca-project-default-rtdb.firebaseio.com",
    "storageBucket": "iotca-project.appspot.com"
    }

firebase = pyrebase.initialize_app(config)
cnt = 0
db = firebase.database()
while not GPIO.input(16):
	try:
		print("test")
		id, text = reader.read()
		cnt += 1
		print(id)
		print(text)
		data = {
            "id" : id,
            "text": text
        }
		label, name = text.split(": ")
		label = label.strip()
		name = name.strip()
		if label == "Professor":
			GPIO.output(18,GPIO.HIGH)
			time.sleep(3)
			GPIO.output(18,GPIO.LOW)
		elif label == "Student":
			GPIO.output(23,GPIO.HIGH)
			time.sleep(3)
			GPIO.output(23,GPIO.LOW)
		else:
			GPIO.output(23,GPIO.HIGH)
			GPIO.output(18,GPIO.HIGH)
			time.sleep(3)
			GPIO.output(18,GPIO.LOW)
			GPIO.output(23,GPIO.LOW)
		current_date = datetime.datetime.now().strftime('%H:%M:%S')
		url="https://api.thingspeak.com/update?api_key=NVO67HD5LZS68Y16&field1={}&field2={}&field3={}".format(current_date, cnt, text)
		reponse=requests.get(url)
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

