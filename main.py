
#Importing Libraries

import cv2
import numpy as np
from datetime import datetime
import face_recognition
import os






'''###########----After This Begins Face Recognition-----############'''


##################----FACE RECOGNITION ATTENDENCE-----########################

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
classMails = []
myList = os.listdir(path)
#print(myList)

#collecting Images
for id in myList:
  currImg = cv2.imread(f'{path}/{id}')
  images.append(currImg)
  classNames.append(id.split('_')[0])
  classMails.append(id.split('_')[1])

print(classNames)
print(classMails)

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
print('Encode Successful')

#Getting Input From Web Cams
cap = cv2.VideoCapture(1)
###########################################################################################
thres = 0.45 # Threshold to detect object

#starting Webcam & Setting it Up
cap2 = cv2.VideoCapture(0)
cap2.set(3,1280)
cap2.set(4,720)
cap2.set(10,70)

#Collecting Names from coco.names
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')


#Importing Configurations and Weights
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

#Initializing and scanning Configurations and Weights
net = cv2.dnn_DetectionModel(weightsPath,configPath)

#Using Default values as given in Documentation
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
########################################################################################

#For Object Detection
count = 0
while True:
  success, img = cap.read()
  imgS = cv2.resize(img,(0,0),None,0.25,0.25)
  imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

  facesCurrFrame = face_recognition.face_locations(imgS)
  encodeCurrFrame = face_recognition.face_encodings(imgS,facesCurrFrame)

  for encodeFaces, faceLoc in zip(encodeCurrFrame,facesCurrFrame):
    matches = face_recognition.compare_faces(encodeListKnown,encodeFaces)
    faceDist = face_recognition.face_distance(encodeListKnown,encodeFaces)

    #print(type(faceLoc))

    matchIndex = np.argmin(faceDist)

    if matches[matchIndex] and count<2:
      name = classNames[matchIndex].upper()
      mail = classMails[matchIndex]
      #print(name)
      y1,x2,y2,x1 = faceLoc
      y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
      cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
      cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
      cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
      markAttendence(name)
      count+=1

###################################################################################################

  success, img2 = cap2.read()

  # Collecting Ids of coco.names & %Accuracy & dimensions
  classIds, confs, bbox = net.detect(img2, confThreshold=thres)
  # print(classIds,bbox)

  if len(classIds) != 0:
      for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
          cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
          cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                      (0, 255, 0), 2)
          # cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)


  #####################################################################################################
  cv2.imshow('Webcam',img)
  #Stop if ESC is pressed
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    cap.release()

  cv2.imshow("Output", img2)
  if cv2.waitKey(1) & 0xff == ord('q'):
      cap2.release()
      break





cv2.destroyAllWindows()