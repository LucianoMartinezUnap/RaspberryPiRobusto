#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from NFC import NfcReader as Nfc
from CAM import CamInterface as Cam
from Connect2DB import Connection2DB as C2B
from usermanager import UserManagement as UserMgt
import time
Path = 'dataset'
Reader = Nfc()
while True:
	try:
		Reader.ReadCard()
		"""
		##Crear usuario
		#//Server almacena cosas
		#//RPi lee la info del nfc
		#//GET desde servidor
		#//RPi crea un dataset de una persona asociandola al nfc
		#//RPi entrena
		#//POST de CUENTA CREADA al servidor

		##Iniciar secion
		#//RPi detecta DISPOSITIVO NFC
		#//POST al servidor
		#//Solicita Reconocimiento facial GET
		#//Si OPENCV.REQFACIAL(CARA.PERSONA) == TRUE == NFC.ASOCIADO entonces POST 'TRUE' al servidor
		#//Dar acceso al sistema
		"""
		#UserMgt.LoginUser(Reader)
		#Create
		#enviar crear, logear y false
		C2B.Post2DB('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Key='nfc', Value = Reader.GetUid())
		print("NFC Checked")
		time.sleep(1)
		Response = C2B.GetProviderConfirmation(Reader.GetUid(), '190.114.253.43', '/MVC/Controller/PHP/endpoint.php')
		Response = Response.read().decode()
		Response = ' '.join(Response.split())
		print(len(Response))
		if Response in 'Logear': 
			UserMgt.LoginUser(Reader)
			continue
		elif Response in 'Crear': 
			UserMgt.RegisterUser(Reader)
			continue
		else:
			print('Respuesta negativa recibida')
		time.sleep(1)
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		raise
	finally:
		GPIO.cleanup()

