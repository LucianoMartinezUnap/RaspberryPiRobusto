#!/usr/bin/env python

import cv2
import numpy as np
import imutils
import os
import time
import ast
import json
def MakeDatasetFolder(Path, Name):
	if not os.path.exists(Path + '/' + Name):
		Folder = os.path.join(Path, Name)
		os.makedirs(Folder)
		print("Carpetas Creadas")


def GapsInFoldersNumeration(Path, Extension = '.jpg'):
	UsedNumbers = set()
	for File in os.listdir(Path):
		if File.endswith(Extension):
			NumberString = File[len(f"imagen_{Extension}") : -len(Extension)]
			if NumberString.isdigit():
				UsedNumbers.add(int(NumberString))
	Number = 1
	while Number in UsedNumbers:
		Number += 1
	return Number

def DeltaTempo(TimeNumber):
	while TimeNumber:
		Minutes, Seconds = divmod(TimeNumber, 60)
		time.sleep(1)
		TimeNumber -= 1
	return True
"""
def FaceDictionaryReader():
	with open('./faces_dict.txt') as File:
		Data = File.read()
	return ast.literal_eval(Data)
def AddNewFace(Name, FilePath, Action):
	with open (FilePath, 'r') as F:
		Data = json.load(F)
	if Name in Data:
		print(f"{Name} already exists in the file.")
		return
	else:
		Data[Name] = {"start_time" : None, "code" : Action}
	with open(FilePath, 'w') as F:
		json.dump(Data, F, indent = 4)
	print(f"{Name} has been added to the file.")


def AddNewFace(Name, FilePath, Code):
	# Open the file in read-binary mode and load the data as a dictionary
	with open(FilePath, 'rb') as f:
		data = pickle.load(f)
		print(data)

	# Check if the name already exists in the data
	if Name in data:
		# If yes, print a message and return
		print(f"{Name} already exists in the file.")
		return
	else:
		# If not, create a new entry for the name with the start_time as None and the code as the argument
		data[Name] = {"start_time": None, "code": Code}
	# Open the file in write-binary mode and dump the updated data as pickle
	with open(FilePath, "wb") as f:
		pickle.dump(data, f)
	# Print a message to confirm the addition
	print(f"{Name} has been added to the file.")
"""

