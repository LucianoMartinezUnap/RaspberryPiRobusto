#!/usr/bin/env python
import cv2
import numpy as np
import imutils
import os

os.system('fswebcam list')

Datos = 'dataset/'
name = 'Ricardo' 
if not os.path.exists(Datos+ '/' +name):
    path = os.path.join(Datos, name)
    os.makedirs(path)
    print("Carpetas creadas")

webcam = cv2.VideoCapture(0)
key = cv2. waitKey(1)

count = 0




while True:
    try:
        check, frame = webcam.read() # Toma la foto y el booleano donde confirma la accion.
        print(check) #prints true as long as the webcam is running
        print(frame) #prints matrix values of each framecd 
        cv2.imshow("Capturing", frame) # abre una ventana donde muestra la camara en funcionamiento.
        key = cv2.waitKey(1) #input
        if key == ord('s'): 
            cv2.imwrite(filename=Datos+ '/' + name + '/imagen{}.jpg'.format(count), img=frame) #guardar la foto
            #webcam.release() Libera la camara pero tambien es como un pseudo destructor, no la habilita mas.
            #img_new = cv2.imread(Datos+ '/' + name + '/imagen{}.jpg'.format(count), cv2.IMREAD_GRAYSCALE)
            img_new = cv2.imshow("Captured Image", img_new)
            cv2.waitKey(1650)
            cv2.destroyAllWindows()
            """
            print("Processing image...")
            img_ = cv2.imread(Datos+ '/' + name + '/imagen{}.jpg'.format(count), cv2.IMREAD_ANYCOLOR)
            print("Converting RGB image to grayscale...")
            gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY) #convertir la foto en escala de grises
            print("Converted RGB image to grayscale...")
            print("Resizing image to 28x28 scale...")
            img_ = cv2.resize(gray,(28,28)) #cambia la resolucion de la imagen a una mas pequeña
            print("Resized...")
            img_resized = cv2.imwrite(filename=Datos+ '/' + name + '/imagenFinal{}.jpg'.format(count), img=img_) #guarda una imagen mas pequeña de la sacada.
            print("Image saved!")
            """
            count += 1 #contador de fotos.
            #break
        elif key == ord('q'):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
        
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
