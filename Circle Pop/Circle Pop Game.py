import cv2
import random
import mediapipe as mp
import time

frameWidth = 1200
frameHeight = 900

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

circles = []
score = 0

start_time = time.time()
game_time = 30

for i in range(8):
    circles.append({
        'x': random.randint(50, frameWidth-50),
        'y': random.randint(480, frameHeight-50),
        'r': random.randint(30 ,35),
        'speed': random.randint(3, 7),
        'color': (random.randint(50,255),
                  random.randint(50,255),
                  random.randint(50,255))})

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)


    if not success:
        print('Failed to access webcam')
        break

    for circle in circles:

        # move upward
        circle['y']= circle['y'] - circle['speed']
        
        if circle['y'] + circle['r'] < 0:
            circle['y'] = frameHeight + circle['r']
            circle['x'] = random.randint(50, frameWidth - 50)
            circle['r'] = random.randint(30, 35)
            circle['speed'] = random.randint(3, 7)
            circle['color'] = (random.randint(50,255),
                  random.randint(50,255),
                  random.randint(50,255))


        cv2.circle(img,(circle['x'], circle['y']),circle['r'],circle['color'],-1)
        # cv2.circle(image, center, radius, color, thickness, filled)


        index_x = None
        index_y = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                mp_draw.draw_landmarks(img,hand_landmarks,mp_hands.HAND_CONNECTIONS)
                h, w, i = img.shape
                index_tip = hand_landmarks.landmark[8]
                index_x = int(index_tip.x * w)
                index_y = int(index_tip.y * h)
                cv2.circle(img, (index_x, index_y), 10, (0, 255, 255), -1)



    cv2.putText(img, f'Score: {score}', (20, 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    elapsed = time.time() - start_time
    remaining = max(0, int(game_time - elapsed))

    cv2.putText(img, f'Time: {remaining}', (20, 100),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    if elapsed >= game_time:
        cv2.putText(img, 'GAME OVER', (130, 340),cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 15)
        # img, text, points to start the text with, font, scale- how big text u want, color, thickness
        cv2.imshow('CIRCLE POP', img)
        cv2.waitKey(3000)
        break
    

    cv2.imshow('CIRCLE POP', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# 4  Thumb tip
# 8  Index finger tip
# 12  Middle finger tip
# 16  Ring finger tip
# 20  Pinky tip