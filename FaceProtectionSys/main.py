import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cap = cv2.VideoCapture(0)
cap.set(3 , 640 )
cap.set(4 , 480 )
cred = credentials.Certificate("serviceAcount.json")
firebase_admin.initialize_app(cred , {
    'databaseURL': "",
    'storageBucket': ""
})
bucket = storage.bucket()

imgBackground = cv2.imread("Resources/background.png")

FolderModePath = "Resources/Modes"
modePathList = os.listdir(FolderModePath)
imgModeList = []
imgStudent = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(FolderModePath , path)))
# loading the encodings file
file = open("EncodeFile.p" , 'rb')
encodeListKnownWithID = pickle.load(file)
file.close()
encodeListKnown , std_ids = encodeListKnownWithID

modeType = 0
cnt = 0
id = -1
while True :
    success , img = cap.read()
    imgs = cv2.resize(img , (0,0) , None , 0.25 , 0.25)
    imgs = cv2.cvtColor(imgs , cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgs)
    encodesCurFrame = face_recognition.face_encodings(imgs , facesCurFrame)




    imgBackground[162:162+480,55:55+640]= img
    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

    for encodeFace , faceLoc in zip(encodesCurFrame , facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown , encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown , encodeFace)
        matchIndex = np.argmin(faceDis)
        if(matches[matchIndex]):
            y1 , x2 , y2 , x1 = faceLoc
            y1 , x2 , y2 , x1 = y1*4 , x2*4 , y2*4 , x1*4
            bbox = 55+ x1 , 162+y1 , x2-x1 , y2-y1
            cvzone.cornerRect(imgBackground , bbox , rt=0)
            id = std_ids[matchIndex]
            if cnt == 0 :
                cnt = 1
                modeType = 1

    if cnt !=0 :

       if cnt == 1:
            studentInfo = db.reference(f"students/{id}").get()
            print(studentInfo)
            blob = bucket.blob(f"Images/{id}.png")
            array = np.frombuffer(blob.download_as_string() , np.uint8)
            imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)

            # update the time
            datetimeObject = datetime.strptime(studentInfo['last attendance'],
                                               "%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
            print(secondsElapsed)

            if(secondsElapsed > 60):
                ref = db.reference(f"students/{id}")
                studentInfo['total attendance'] += 1
                ref.child('total attendance').set(studentInfo['total attendance'])
                ref.child('last attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else :
                modeType = 3
                cnt = 0
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


       if 10<cnt<20:
           modeType = 2

       imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

       if modeType != 3:
           if cnt <=10:
               cv2.putText(imgBackground , str(studentInfo['total attendance']) , (861 , 125) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255,255,255) , 1)
               (w , h ) , _ = cv2.getTextSize(str(studentInfo['name']) , cv2.FONT_HERSHEY_COMPLEX , 1 , 1)
               offset = (414 - w) // 2
               cv2.putText(imgBackground , str(studentInfo['name']) , (808+offset , 445) , cv2.FONT_HERSHEY_COMPLEX , 1 , (50,50,50) , 1)
               cv2.putText(imgBackground , str(studentInfo['major']),   (1006 , 550) , cv2.FONT_HERSHEY_COMPLEX ,0.5, (255,255,255),1  , 1)
               cv2.putText(imgBackground , str(id) , (1006 , 493), cv2.FONT_HERSHEY_COMPLEX , 0.5, (255,255,255),1  , 1)
               cv2.putText(imgBackground , str(studentInfo['standing']) , (910 , 625) , cv2.FONT_HERSHEY_COMPLEX , 1 , (100,100,100) , 1)
               cv2.putText(imgBackground , str(studentInfo['year']) , (1025 , 625) , cv2.FONT_HERSHEY_COMPLEX , 1 , (100,100,100) , 1)
               cv2.putText(imgBackground , str(studentInfo['starting year']) , (1125 , 625) , cv2.FONT_HERSHEY_COMPLEX , 1 , (100,100,100) , 1)
               imgBackground[175:175+216, 909:909+216] = imgStudent
           cnt+=1

           if cnt >= 20:
                cnt = 0
                modeType = 0
                studentInfo = {}
                imgStudent = []
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
       else:
           cnt = 0
           modeType = 0




    cv2.imshow("Face Attendence " , imgBackground)

    cv2.waitKey(1)
