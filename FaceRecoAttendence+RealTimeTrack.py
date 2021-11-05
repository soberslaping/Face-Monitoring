
#Importing Libraries

import cv2
import numpy as np
from datetime import datetime
import face_recognition

import os

#Marking Attendence
def markAttendence(name):
  with open('Attendence.csv','r+') as f:
    myDataList = f.readlines()
    nameList = []
    for line in myDataList:
      entry = line.split(',')
      nameList.append(entry[0])
    if name not in nameList:
      now = datetime.now()
      dtString = now.strftime('%H:%M:%S')
      f.writelines((f'\n{name},{dtString}'))

#importing images one by one

path = 'ImageBasic'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

#collecting Images
for cl in myList:
  currImg = cv2.imread(f'{path}/{cl}')
  images.append(currImg)
  classNames.append(os.path.splitext(cl)[0])

print(classNames)

#Finding Encodings
def findEncodings(images):
  encodeList = []
  for img in images:
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    encodeList.append(encode)
  return encodeList

#Checking if encoding is Done
encodeListKnown = findEncodings(images)
print(len(encodeListKnown))

#Getting Input From Web Cams
cap = cv2.VideoCapture(0)

#Creating Traker
tracker = cv2.TrackerCSRT_create()
success, img = cap.read()
bbox = cv2.selectROI("Webcam",img,False)
tracker.init(img,bbox)

while True:
  success, img = cap.read()

  #Trying of Tracking
  success, bbox = tracker.update(img)
  if success:
      cv2.putText(img, "Present", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
  else:
      cv2.putText(img, "Absent", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

  imgS = cv2.resize(img,(0,0),None,0.25,0.25)
  imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

  facesCurrFrame = face_recognition.face_locations(imgS)
  encodeCurrFrame = face_recognition.face_encodings(imgS,facesCurrFrame)

  for encodeFaces, faceLoc in zip(encodeCurrFrame,facesCurrFrame):
    matches = face_recognition.compare_faces(encodeListKnown,encodeFaces)
    faceDist = face_recognition.face_distance(encodeListKnown,encodeFaces)

    #print(faceDist)

    matchIndex = np.argmin(faceDist)

    if matches[matchIndex]:
      name = classNames[matchIndex].upper()
      #print(name)
      y1,x2,y2,x1 = faceLoc
      y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
      cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
      cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
      cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
      markAttendence(name)



  cv2.imshow('Webcam',img)

  #Stop if ESC is pressed
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break;

cap.release()

'''
import cv2

cap = cv2.VideoCapture(1)

def drawBox(img,bbox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2,1)
    cv2.putText(img, "Present", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

tracker = cv2.TrackerCSRT_create()
success, img = cap.read()
bbox = cv2.selectROI("Webcam",img,False)
tracker.init(img,bbox)
while True:
    timer = cv2.getTickCount()
    success, img = cap.read()

    success, bbox = tracker.update(img)
    if success:
        drawBox(img,bbox)
    else:
        cv2.putText(img,"Absent",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,255),2)
    cv2.imshow('Webcam',img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
'''