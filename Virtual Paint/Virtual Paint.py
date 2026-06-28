import cv2

framewidth = 700
frameheight = 500

cap = cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,130)


while True:
    sucess, img = cap.read()
    cv2.imshow('mywebcam', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

