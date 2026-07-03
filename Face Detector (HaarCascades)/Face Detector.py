# IMAGE FACE DETECTOR

import cv2

faceCascade = cv2.CascadeClassifier(r'C:\Users\Chelsi\Downloads\haarcascades (3)\haarcascades\haarcascade_frontalface_default.xml')
# pre trained machine learning model
# xml file --> cascade classifier --> ready to use

img = cv2.imread(r'C:\Users\Chelsi\Downloads\istockphoto-1166662691-1024x1024.jpg')
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# we had to covert the image to gray scale cause face detection dont need blue green red channels it only needs brightness
# if color image is 500,500,3 then gray image 500,500 there is no channels only rows and columns

faces = faceCascade.detectMultiScale(imgGray, 1.1 , 4)
# face can be large small thats why we use multiscale
# scale factor --> 1.1
# if scale factor less then more accurate and more scales checked, slower
# if scale factor more like 1.3 then few scales face can miss, faster
# minNeighbours --> 4
# few false positive if high values
# more false positive if low values

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)


cv2.imshow('FACE DETECTOR', img)
cv2.waitKey(0)





# WEBCAM FACE DETECTOR

import cv2

faceCascade = cv2.CascadeClassifier(r'C:\Users\Chelsi\Downloads\haarcascades (3)\haarcascades\haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Face Detector', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()





# VIDEO FACE DETECTOR

import cv2

faceCascade = cv2.CascadeClassifier(r'C:\Users\Chelsi\Downloads\haarcascades (3)\haarcascades\haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(r'C:\Users\Chelsi\Downloads\myvideo.mp4')

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Face Detector', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()