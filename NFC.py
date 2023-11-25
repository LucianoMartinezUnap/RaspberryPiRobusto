#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

class NfcReader:
	__Name = None
	__Uid = None
	def __init__(self):
		pass
	def ReadCard(self):
		self.__Uid, self.__Name = SimpleMFRC522().read()
	def WriteCard(self, Text):
		self.__Uid, self.__Name = SimpleMFRC522().write(Text)
	def SetName(self, Name):
		self.__Name = Name
	def GetName(self):
		return self.__Name
	def GetUid(self):
		return self.__Uid
