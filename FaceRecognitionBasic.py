#Importing Libraries

import cv2
import numpy as np
import face_recognition

#Taking Image & Converting it from BGR to RGB

imgModi = face_recognition.load_image_file('ImageBasic/modi_pratyush3141@gmail.com_.jpg')
imgModi = cv2.cvtColor(imgModi,cv2.COLOR_BGR2RGB)

imgTest = face_recognition.load_image_file('modiTest.jpg')
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)

#Detecting Face for imgModi
faceLoc = face_recognition.face_locations(imgModi)[0]
faceEncode = face_recognition.face_encodings(imgModi)[0]

#Making Rectangle Around Face
cv2.rectangle(imgModi,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)

#Detecting Face for imgTest
faceLocTest = face_recognition.face_locations(imgTest)[0]
faceEncodeTest = face_recognition.face_encodings(imgTest)[0]

#Making Rectangle Around Face
cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)

#Comparing Images
result = face_recognition.compare_faces([faceEncode],faceEncodeTest)
print(result)

#For Better Correctness Checking the distances between faces
faceDist = face_recognition.face_distance([faceEncode],faceEncodeTest)
#printing Result and Distance at top Left Corner
cv2.putText(imgTest,f'{result} {round(faceDist[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),2)

cv2.imshow('Image',imgModi)
cv2.imshow('TestImage',imgTest)
cv2.waitKey(0)