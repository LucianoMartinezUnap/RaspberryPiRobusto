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
			Copy = Frame.copy()
			text = "Listo para tomar foto oprima 's' para guardar y\\npara finalizar el proceso oprima 'q'."
			textSize, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
			lineHeight = textSize[1] + 5
			# Dividir el texto en líneas y mostrar cada una
			y0, dy = 30, 4 # Puedes cambiar estos valores
			for i, line in enumerate(text.split("\\n")):
				y = y0 + i * lineHeight
				cv2.putText(Copy, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
			# Mostrar la copia con texto
			cv2.imshow("Capturing", Copy)

			Key = cv2.waitKey(1)
			if Key == ord('s'):	
				if not Flag:
					cv2.imwrite(filename=Path + '/' + Name + '/imagen_{}.jpg'.format(Count), img=Frame)
				else:
					Count = GapsInFoldersNumeration(Path  + '/' + Name)
					cv2.imwrite(filename=Path + '/' + Name + '/imagen_{}.jpg'.format(Count), img=Frame)
				cv2.waitKey(1650)
				cv2.destroyAllWindows()
				empty_image = np.zeros(Frame.shape, dtype=np.uint8)
				font = cv2.FONT_HERSHEY_SIMPLEX # Elegimos el tipo de fuente
				color = (0, 255, 0) # Elegimos el color verde
				thickness = 2 # Elegimos el grosor de la línea
				text = f"Foto {Count}" # Creamos el texto con el número de la foto
				org = (Frame.shape[1] - 200, 50) # Elegimos la posición del texto en la esquina superior derecha
				# Usamos el método cv2.putText() para dibujar el texto en la imagen vacía
				cv2.putText(empty_image, text, org, font, 1, color, thickness, cv2.LINE_AA)
				# Mostramos la imagen vacía con el texto en la misma ventana que la imagen capturada
				cv2.imshow("Capturing", empty_image)
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
		print(Data['names'])
		timestamp = datetime.datetime.now()
		start_time = None
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
					
				if Name in Data['names'] and Name == str(CardId):
					FaceDetected = True
					#timestamp = None
					# get the start time and the code for the face
					# if the start time is None, set it to the current time
					if start_time is None:
						start_time = datetime.datetime.now()
					# calculate the time difference between the current time and the start time
					time_diff = (datetime.datetime.now() - start_time).total_seconds() ###Vulnerabilidad, una persona puede estar por un segundo y regresar tiempo despues y el sistema lo sigue contemplando, no hay reinicio de este contador
					# if the time difference is greater than or equal to the wait time, run the code
					if time_diff >= wait_time:
						print(f"bienvenido {Name}")
						#aqui se puede agregar codigo personalizado cuando se confirma el reconocimiento facial
						# reset the start time to None
						start_time = None
						Fps.stop()
						print("[INFO] elasped time: {:.2f}".format(Fps.elapsed()))
						print("[INFO] approx. FPS: {:.2f}".format(Fps.fps()))
						cv2.destroyAllWindows()
						VS.stop()

						return True
			if not FaceDetected:
				start_time = None
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


