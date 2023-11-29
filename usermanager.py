import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from NFC import NfcReader as Nfc
from CAM import CamInterface as Cam
from Connect2DB import Connection2DB as C2B
import time

Path = 'dataset'
class UserManagement:
	
	def LoginUser(Card):
		#Envio de la informacion de la tarjeta a la base de datos		
		C2B.Post2DB('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Key='nfc', Value = Card.GetUid())
		print("NFC Checked")
		time.sleep(1)
		
		if C2B.GetProviderConfirmation(Card.GetUid(), '190.114.253.43', '/MVC/Controller/PHP/endpoint.php') == True:
			Flag = Cam.FacialRecog(Card.GetUid()) # reconocimiento facial
			C2B.Post2DB('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Key='rf', Value = Flag) #enviar al servidor una confirmacion del login
		else:# Si el código de estado no es 200
			print('Respuesta negativa recibida') # Imprimir respuesta negativa
		time.sleep(1)
		
		
	def RegisterUser(Card):
		#sacar fotos
		#
		Cam.TakeManualPhoto(Path, str(Card.GetUid()))
		print("Preparando entrenamiento facial")
		Cam.TrainingModels()
		C2B.Post2DB('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Key='nfc', Value = Card.GetUid())
		
