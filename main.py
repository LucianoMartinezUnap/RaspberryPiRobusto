#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from NFC import NfcReader as Nfc
from CAM import CamInterface as Cam
from Connect2DB import Connection2DB as C2B
from usermanager import UserManagement as User
import time
Path = 'dataset'
Reader = Nfc()
while True:
	try:
		Reader.ReadCard()
		"""
		#Paso 1
		Reader.ReadCard()
		#Cam.TakeManualPhoto('dataset/', str(Reader.GetUid()))
		
		C2B.Post2DB('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Key='nfc', Value = Reader.GetUid())
		
		print("NFC Checked")
		time.sleep(1)
		#Cam.TrainingModels()
		#Paso 2
		if C2B.GetProviderConfirmation(Reader.GetUid(), '190.114.253.43', '/MVC/Controller/PHP/endpoint.php') == True:
			Flag = Cam.FacialRecog(Reader.GetUid())
			C2B.Post2DB('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Key='rf', Value = Flag)
		
		else:# Si el código de estado no es 200
			print('Respuesta negativa recibida') # Imprimir otro mensaje.
		time.sleep(1)
			# Manejar el error o volver a intentar
        #conn.close() # Cerrar la conexión

		
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
		User.LoginUser(Reader)
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		raise
	finally:
		GPIO.cleanup()

