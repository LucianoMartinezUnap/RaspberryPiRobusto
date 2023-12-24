#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from NFC import NfcReader as Nfc
from CAM import CamInterface as Cam
from Connect2DB import Connection2DB as C2B
from usermanager import UserManagement as UserMgt
import time
import json
import os
Path = 'dataset'
Reader = Nfc()
AdminNFCUID = 189074271987
#AdminNFCUID = "[Ingrese aqui la uid del admin]"
def strip(String):
	String = ' '.join(String.split())
	x = String.split(":")
	return x
"""
def Convert2Dict(KeysValue):
	auxdict = {}
	for key, value in KeysValue:
		if key not in auxdict:
			auxdict[key] = []
		auxdict[key].append(value)
	return auxdict
"""
while True:
	try:
		print("leyendo la nfc")
		Reader.ReadCard()  
		#print(Reader.GetUid())
		#enviar crear, logear y false
		#if Reader.GetUid() is not AdminNFCUID:
		Response = C2B.Post2DB('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Key='nfc', Value = Reader.GetUid())

		#print(Response.read().decode()) #mantener response
		AuxResponse = Response.read().decode()
		print(AuxResponse)
		Status = strip(AuxResponse)
		#print(Status)
		
		#cada condicional mas limpio en usermanager.py
		
		if Status[0] in 'Create':
			time.sleep(1)
			print("ingrese una nueva nfc")
			Reader.ReadCard()
			foo = {'nfcCreate': Reader.GetUid(), 'nfcAdmin': Status[1]}
			r2 = C2B.Post2DBDict('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Dictionary= foo)
			print(r2.read().decode())
			#UserMgt.RegisterUser(Reader)
			print("exito")
		elif Status[0] in 'Update':
			time.sleep(1)
			print("ingrese una nueva nfc")
			Reader.ReadCard()
			foo = {'nfcUpdate': Reader.GetUid(), 'nfcAdmin': Status[1]}
			os.rename(Path + f'/{Status[2]}', Path + f'/{Reader.GetUid()}')
			Cam.TrainingModels()
			r2 = C2B.Post2DBDict('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Dictionary= foo)
			print(r2.read().decode())
			print("exito actualizado")
		elif Status[0] in 'Login':
			UserMgt.LoginUser(Reader)
			print("exito logeado")
	
		#cambiar el directorio en update con la nueva nfc
		"""
		if Reader.GetUid() == AdminNFCUID:
			time.sleep(1)
			Reader.ReadCard()  
			UserMgt.RegisterUser(Reader)
		"""
		'''print("NFC Checked")
		time.sleep(1)
		Response = Response.read().decode()
		Response = ' '.join(Response.split())
		print(Response)
		if Response in 'Logear': 
			UserMgt.LoginUser(Reader)
			continue
		elif Response in 'Crear': 
			#if Reader.GetUid() is not AdminNFCUID:
			UserMgt.RegisterUser(Reader)
			continue
		elif Response in 'False':
			print('Respuesta negativa recibida')
		'''
		#print(Reader.GetUid())
		time.sleep(1)
	except Exception as err:
		print(f"Unexpected {err=}, {type(err)=}")
		raise
	finally:
		GPIO.cleanup()




