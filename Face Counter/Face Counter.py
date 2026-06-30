import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
# loaded face detection module
# mp.solutions has many solutions like
    #-- hands
    #-- pose
    #-- face_mesh
    #-- face_detection

face_detection = mp_face_detection.FaceDetection(model_selection=0,min_detection_confidence=0.5)
# model_selection = 0   if fast and 2 metres away 
# model_selection = 1   if 5 metres away long distance slow
# min_detection_confidence = ranges from 0.0 --> 1.0

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        print('cannot detect the camera')
        break

    frame = cv2.flip(frame, 1)
    # flip the image
    # if 0 then vertical flip
    # if 1 then horizontal flip
    # if -1 then both the direction
    
    h, w, _ = frame.shape
    # height at h,width as w, _ as channels
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb)
    # since opencv stores the image as bgr but mediapipe expects rgb so we need to convert
    # in results it will look at image and predict faces

    face_count = 0

    if results.detections:
        face_count = len(results.detections)

        for detection in results.detections:
            box = detection.location_data.relative_bounding_box
            # mediaipipe stores xmin ymin height width and their value btw 0 to 1
            # eg xmin=0.3 means 30% from left
            # gr ymin=0.25 means 25% from bottom

            x = int(box.xmin * w)
            # 300 = (0.3*1000) face will start from 300
            y = int(box.ymin * h)
            bw = int(box.width * w)
            bh = int(box.height * h)

            cv2.rectangle(frame,(x, y),(x + bw, y + bh),(255, 0, 255),2)
            # x,y top left corner of face, x+bw+y+bh bottom right corner of face, color in bgr, line thickness


    cv2.putText(frame,f'Faces: {face_count}',(20, 40),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),2)
    cv2.imshow('FACE COUNTER', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()