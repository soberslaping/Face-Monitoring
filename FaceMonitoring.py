import cv2
import time

#loading cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#To capture Video From WebCam
cap = cv2.VideoCapture(0)

total_time = 0
presence_time = 0

while True:
    _, img = cap.read()

    #Converting image to gray
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #Detect Faces
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    '''
    if faces == ():
        t = time.strftime('%Y-%M-%D_%H:%M:%S')
        print('Absent at :  '+t)
        count+=1
    '''
    #draw rectangle around Faces
    for x,y,w,h in faces:

        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

        #display
        cv2.imshow('Webcam',img)
        t = time.strftime('%Y-%M-%D_%H:%M:%S')
        print('Present at '+t)
        #file = 'FaceMonitor'+t+'.jpg'
        #cv2.imwrite(file,img)

        presence_time+=1


    total_time+=1
    #Stop if q is pressed
    #k = cv2.waitKey(1) & 0xff==ord('q'):

    if cv2.waitKey(1) & 0xff==ord('q'):
        print('Total Class Time :',round(total_time/10,2),' seconds',round(total_time/600,2),' minutes\n'
              'Total Presence Time : ',round(presence_time/10,2),' seconds',round(presence_time/600,2),' minutes')
        if (presence_time*100)/total_time > 50:
            print('Attendence Marked!')
        break

#Release Video Capture Object
cap.release()
cv2.destroyAllWindows()