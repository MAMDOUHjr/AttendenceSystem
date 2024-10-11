import os
import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("serviceAcount.json")
firebase_admin.initialize_app(cred , {
    'databaseURL': "",
    'storageBucket': ""
})


FolderPath = "Images"
PathList = os.listdir(FolderPath)
imgList = []
std_ids = []
for path in PathList:
    std_ids.append(os.path.splitext(path)[0])
    imgList.append(cv2.imread(os.path.join(FolderPath , path)))

    file_name  =  f"{FolderPath}/{path}"
    buket = storage.bucket()
    blob = buket.blob(file_name)
    blob.upload_from_filename(file_name)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding Started.....")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithID = [encodeListKnown , std_ids]
# print(encodeListKnown)
print("Encoding Completed.....")


file  = open("EncodeFile.p" , 'wb')
pickle.dump(encodeListKnownWithID , file)
file.close()
print("File Saved.....")
