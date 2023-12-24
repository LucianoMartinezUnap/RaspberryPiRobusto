import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from NFC import NfcReader as Nfc
from CAM import CamInterface as Cam
from Connect2DB import Connection2DB as C2B
import time

Path = 'dataset'
class UserManagement:
	
	def LoginUser(Card):
		Flag = Cam.FacialRecog(Card.GetUid()) # reconocimiento facial
		C2B.Post2DB('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Key='rf', Value = Flag) #enviar al servidor una confirmacion del login
		#post keyrf  
		#(Opcional) luz led para indicar que se logro
	def RegisterUser(Card):
		print("Listo para tomar foto oprima 's' para guardar y\npara finalizar el proceso oprima 'q'.")
		Cam.TakeManualPhoto(Path, str(Card.GetUid()))
		print("Preparando entrenamiento facial")
		Cam.TrainingModels()
		C2B.Post2DB('190.114.253.43', 80, '/MVC/Controller/PHP/endpoint.php', Key='lectura', Value = True)
