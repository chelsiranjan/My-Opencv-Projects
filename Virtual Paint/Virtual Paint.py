import cv2
import mediapipe as mp
import numpy as np

framewidth = 1280
frameheight = 720

xp, yp = 0, 0

canvas = np.zeros((frameheight, framewidth, 3), np.uint8)
drawColor = (0, 0, 255)

brushthickness = 5
eraserthickness = 100

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,max_num_hands=1,min_detection_confidence=0.5,min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,130)


def colorbar(img):
    colors = [
        ((100, 50), (0, 0, 255)),      # red
        ((180, 50), (0, 255, 255)),    # yellow
        ((260, 50), (0, 255, 0)),      # green
        ((340, 50), (255, 0, 255)),    # pink
        ((420, 50), (255, 0, 0)),      # blue
        ((500, 50), (153, 50, 204)),   # purple
        ((580, 50), (89, 89, 89))]     # gray

 
    for center, color in colors:
        if color == drawColor:
            cv2.circle(img, center, 35, color, cv2.FILLED)
            cv2.circle(img, center, 39, (255, 255, 255), 3)
        else:
            cv2.circle(img, center, 30, color, cv2.FILLED)
            # centre point, radius, color, thickness


while True:
    success, img = cap.read()

    if not success:
        print('cannot detect webcam')
        break

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    colorbar(img)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img,hand_landmarks,mp_hands.HAND_CONNECTIONS)
            h, w, c = img.shape

            index_tip = hand_landmarks.landmark[8]
            index_x = int(index_tip.x * w)
            index_y = int(index_tip.y * h)


            if index_y < 80:

                if 70 < index_x < 130:
                    drawColor = (0, 0, 255)     

                elif 150 < index_x < 210:
                    drawColor = (0, 255, 255)  

                elif 230 < index_x < 290:
                    drawColor = (0, 255, 0)     

                elif 310 < index_x < 370:
                    drawColor = (255, 0, 255)  

                elif 390 < index_x < 450:
                    drawColor = (255, 0, 0)     

                elif 470 < index_x < 530:
                    drawColor = (153, 50, 204)   

                elif 550 < index_x < 610:
                    drawColor = (89, 89, 89)  

                elif 640 < index_x < 772:
                    canvas = np.zeros((frameheight, framewidth, 3), np.uint8)
                    # new canvas if clicking on clear
                    cv2.rectangle(img, (640, 15), (772, 75), (255, 255, 255), 10)


                elif 800 < index_x < 960:
                    drawColor = (0, 0, 0)
                    # black eraser
                    cv2.rectangle(img, (800, 15), (960, 75), (255, 255, 255), 10)


            else:
                if xp == 0 and yp == 0:
                    xp, yp = index_x, index_y

                if drawColor == (0, 0, 0):
                    thickness = eraserthickness
                else:
                    thickness = brushthickness

                cv2.line(canvas, (xp,yp), (index_x,index_y), drawColor, thickness)        
                xp, yp = index_x, index_y

            cv2.circle(img, (index_x, index_y), 12, drawColor, cv2.FILLED)
            cv2.circle(img, (index_x, index_y), 16, (255, 255, 255), 2)


    else:
        xp, yp = 0, 0


    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    mask = gray > 0
    img[mask] = canvas[mask]


    cv2.rectangle(img, (640, 15), (772, 75), (50, 50, 50), cv2.FILLED)
    cv2.putText(img, 'Clear', (659, 58),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 2)

    cv2.rectangle(img, (800, 15), (960, 75), (50, 50, 50), cv2.FILLED)
    cv2.putText(img, 'Eraser', (822, 58),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 2)

    cv2.imshow('VIRTUAL PAINT', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

imgresult = img.copy()

cap.release()
cv2.destroyAllWindows()