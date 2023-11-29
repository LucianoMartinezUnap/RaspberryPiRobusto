#!/usr/bin/env python
import cv2
import numpy as np
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import os
from FolderUtils import *
import datetime
from imutils import paths


class CamInterface:
	def __init__(self):
		pass
	def TakePhoto(Path, Name):
		MakeDatasetFolder(Path, Name) #formato preferible Path = 'dataset/', Name='nombre'
		Cam=cv2.VideoCapture(0) 
		Check, Frame = Cam.read()
		cv2.imshow("Capturing", Frame)

		Flag = False
		if not os.listdir(Path + '/' + Name):
			Count = 1
			Flag = False
		else:
			Count = GapsInFoldersNumeration(Path + '/' + Name)
			Flag = True

		if not Flag:
			for i in range(Count, Count + 12):
				cv2.imwrite(filename=Path + '/' + Name + '/imagen_{}.jpg'.format(Count), img=frame)
		else:
			for AuxCounter in range(1, 12):
				Count = GapsInFoldersNumeration(Path  + '/' + Name) 
				cv2.imwrite(filename=Path + '/' + Name + '/imagen_{}.jpg'.format(Count), img=frame)

		cv2.destroyAllWindows()
	
	def TakeManualPhoto(Path, Name):
		MakeDatasetFolder(Path, Name) #formato preferible Path = 'dataset/', Name='nombre'
		Flag = False
		if not os.listdir(Path + '/' + Name):
			Count = 1
			Flag = False
		else:
			Count = GapsInFoldersNumeration(Path + '/' + Name)
			Flag = True
		Cam=cv2.VideoCapture(0)
		while True:			
			Check, Frame = Cam.read()
			cv2.imshow("Capturing", Frame)
			Key = cv2.waitKey(1)
			if Key == ord('s'):	
				if not Flag:
					cv2.imwrite(filename=Path + '/' + Name + '/imagen_{}.jpg'.format(Count), img=Frame)
				else:
					Count = GapsInFoldersNumeration(Path  + '/' + Name)
					cv2.imwrite(filename=Path + '/' + Name + '/imagen_{}.jpg'.format(Count), img=Frame)
				cv2.waitKey(1650)
				cv2.destroyAllWindows()
				Count += 1
			elif Key == ord('q'):
				print("Turning off camera.")
				Cam.release()
				print("Camera off.")
				print("Program ended.")
				#AddNewFace(Name, './faces_dict.txt', '"print(\'Hello, {0}!\')".format(Name)')
				cv2.destroyAllWindows()
				break
		
	
	def FacialRecog(CardId):
		wait_time = 5
		final_time = 20
		CurrentPerson = "unknown"

		EncodingsP = "encodings.pickle"
		print("[INFO] loading encodings + face detector...")
		Data = pickle.loads(open(EncodingsP, "rb").read())

		VS = VideoStream(src = 0, framerate = 30, resolution = (640, 480)).start()
		time.sleep(2.0)

		Fps = FPS().start()
		
		face_code = FaceDictionaryReader()
		timestamp = datetime.datetime.now()
		while True:
			Frame = VS.read()
			Frame = imutils.adjust_brightness_contrast(Frame, contrast = 65) #70 caso extremo de contraste
			Frame = imutils.resize(Frame, width = 500)

			Boxes = face_recognition.face_locations(Frame)

			Encodings = face_recognition.face_encodings(Frame, Boxes)
			Names = []
			for Encoding in Encodings:

				Matches = face_recognition.compare_faces(Data["encodings"], Encoding, tolerance=0.48)

				Name = "Unknown"

				if True in Matches:

					MatchedIdxs = [i for (i, b) in enumerate(Matches) if b]
					Counts = {}

					for i in MatchedIdxs:
						Name = Data["names"][i]
						Counts[Name] = Counts.get(Name, 0) + 1

					Name = max(Counts, key = Counts.get)

					if CurrentPerson != Name:
						CurrentPerson = Name
						print(CurrentPerson)
						
				Names.append(Name)
			FaceDetected = False
			for((Top, Right, Bottom, Left), Name) in zip(Boxes, Names):
				cv2.rectangle(Frame, (Left, Top), (Right, Bottom),
					(0, 255, 225), 2)
				Y = Top - 15 if Top - 15 > 15 else Top + 15
				cv2.putText(Frame, Name, (Left, Y), cv2.FONT_HERSHEY_SIMPLEX,
					.8, (0, 255, 255), 2)
					
				if Name in face_code and Name == str(CardId):
					FaceDetected = True
					#timestamp = None
					# get the start time and the code for the face
					start_time = face_code[Name]["start_time"]
					code = face_code[Name]["code"]

					# if the start time is None, set it to the current time
					if start_time is None:
						start_time = datetime.datetime.now()
						face_code[Name]["start_time"] = start_time
					# calculate the time difference between the current time and the start time
					time_diff = (datetime.datetime.now() - start_time).total_seconds() ###Vulnerabilidad, una persona puede estar por un segundo y regresar tiempo despues y el sistema lo sigue contemplando, no hay reinicio de este contador
					# if the time difference is greater than or equal to the wait time, run the code
					if time_diff >= wait_time:
						# use the exec function to execute the code as a string
						exec(code)

						# reset the start time to None
						face_code[Name]["start_time"] = None
						Fps.stop()
						print("[INFO] elasped time: {:.2f}".format(Fps.elapsed()))
						print("[INFO] approx. FPS: {:.2f}".format(Fps.fps()))
						cv2.destroyAllWindows()
						VS.stop()

						return True
			if not FaceDetected:
				for Name in face_code:
					face_code[Name]["start_time"] = None
				timedelta = (datetime.datetime.now() - timestamp).total_seconds()
				if timedelta >= final_time:
					Fps.stop()
					print("[INFO] elasped time: {:.2f}".format(Fps.elapsed()))
					print("[INFO] approx. FPS: {:.2f}".format(Fps.fps()))
					cv2.destroyAllWindows()
					VS.stop()
					return False  
				
				
			cv2.imshow("Facial Recognition is Running", Frame)
			Key = cv2.waitKey(1) & 0xFF

			if Key == ord("q"):
				break

			Fps.update()
		Fps.stop()
		print("[INFO] elasped time: {:.2f}".format(Fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(Fps.fps()))
		cv2.destroyAllWindows()
		VS.stop()
		return False
	def TrainingModels():
		# our images are located in the dataset folder
		print("[INFO] start processing faces...")
		imagePaths = list(paths.list_images("dataset"))

		# initialize the list of known encodings and known names
		knownEncodings = []
		knownNames = []

		# loop over the image paths
		for (i, imagePath) in enumerate(imagePaths):
			# extract the person name from the image path
			print("[INFO] processing image {}/{}".format(i + 1,
				len(imagePaths)))
			name = imagePath.split(os.path.sep)[-2]

			# load the input image and convert it from RGB (OpenCV ordering)
			# to dlib ordering (RGB)
			image = cv2.imread(imagePath)
			rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

			# detect the (x, y)-coordinates of the bounding boxes
			# corresponding to each face in the input image
			boxes = face_recognition.face_locations(rgb,
				model="hog")

			# compute the facial embedding for the face
			encodings = face_recognition.face_encodings(rgb, boxes)

			# loop over the encodings
			for encoding in encodings:
				# add each encoding + name to our set of known names and
				# encodings
				knownEncodings.append(encoding)
				knownNames.append(name)

		# dump the facial encodings + names to disk
		print("[INFO] serializing encodings...")
		data = {"encodings": knownEncodings, "names": knownNames}
		f = open("encodings.pickle", "wb")
		f.write(pickle.dumps(data))
		f.close()


