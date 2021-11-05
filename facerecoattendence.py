
#Importing Libraries

import cv2
import numpy as np
from datetime import datetime
import face_recognition
import SendEmail
import os
import Login
from tkinter import *
import wikipedia




#Authorization
Login.Login()


'''  ########### -----  CODE FOR TOOL BOX BEGINS  ------ #############   '''

#ToolBar
def getResult():
    querieEntered = entry.get()
    answer.delete(1.0, END)
    try:
      ansObt = wikipedia.summary(querieEntered)
      answer.insert(INSERT, ansObt)
    except:
      answer.insert(INSERT, "Try Again\nEither you miss-spelled or your internet Connection is Poor")


def onClick(arg):
  if arg == 1:
    os.system('calc')
  elif arg == 2:
    os.system('notepad')


root = Tk()
root.geometry('300x260')
root.title('TOOLBOX')
#photo2 = PhotoImage(file = 'LOGO.png')
#photo = Label(root, image = photo2, bg = 'white')
topframe = Frame(root)
entry = Entry(topframe)
entry.pack()

btn1 = Button(root, text='Calculator', command=lambda: onClick(1))
btn2 = Button(root, text='Notepad', command=lambda: onClick(2))
button = Button(topframe, text="search", command=getResult)

btn1.pack()
btn2.pack()
button.pack()

topframe.pack(side=TOP)

bottomframe = Frame(root)

scroll = Scrollbar(bottomframe)
scroll.pack(side=RIGHT, fill=Y)
answer = Text(bottomframe, width=30, height=10, yscrollcommand=scroll.set, wrap=WORD)
answer.pack()

bottomframe.pack()

'''###########----After This Begins Face Recognition-----############'''


##################----FACE RECOGNITION ATTENDENCE-----########################

#Marking Attendence
def markAttendence(name,mail):
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
      SendEmail.sendEmail(name,mail)




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
cap = cv2.VideoCapture(0)
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
      markAttendence(name,mail)
      count+=1

  cv2.imshow('Webcam',img)
  #Stop if ESC is pressed
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break;



root.mainloop()
cap.release()
cv2.destroyAllWindows()