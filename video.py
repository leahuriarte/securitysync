import cv2
import dlib
from scipy.spatial import distance
from app import *

#Function calculating the aspect ratio for the eye by using euclidean distance function
def Detect_Eye(eye):
	poi_A = distance.euclidean(eye[1], eye[5])
	poi_B = distance.euclidean(eye[2], eye[4])
	poi_C = distance.euclidean(eye[0], eye[3])
	aspect_ratio_Eye = (poi_A+poi_B)/(2*poi_C)
	return aspect_ratio_Eye

def recordVideo(window):
    cap = cv2.VideoCapture(1)

    #face detection or mapping the face to
    # get the eye and eyes detected
    face_detector = dlib.get_frontal_face_detector()

    #put the location of .Dat file (File for
    #predicting the landmarks on face )
    dlib_facelandmark = dlib.shape_predictor("shape_predictor.dat")

    count = 0
    instances = 0

    for i in range(214):

        null, frame = cap.read()
        gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector(gray_scale)
        if len(faces) == 0:
            window.update("No face detected. Ride navigation \nwill not begin.")
            print("nes")

        for face in faces:
            face_landmarks = dlib_facelandmark(gray_scale, face)
            leftEye = []
            rightEye = []

            # THESE ARE THE POINTS ALLOCATION FOR THE
            # LEFT EYES IN .DAT FILE THAT ARE FROM 42 TO 47
            for n in range(42, 48):
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                rightEye.append((x, y))
                next_point = n+1
                if n == 47:
                    next_point = 42
                x2 = face_landmarks.part(next_point).x
                y2 = face_landmarks.part(next_point).y
                cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)

            # THESE ARE THE POINTS ALLOCATION FOR THE
            # RIGHT EYES IN .DAT FILE THAT ARE FROM 36 TO 41
            for n in range(36, 42):
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                leftEye.append((x, y))
                next_point = n+1
                if n == 41:
                    next_point = 36
                x2 = face_landmarks.part(next_point).x
                y2 = face_landmarks.part(next_point).y
                cv2.line(frame, (x, y), (x2, y2), (255, 255, 0), 1)

            # calculate aspect ration
            right_Eye = Detect_Eye(rightEye)
            left_Eye = Detect_Eye(leftEye)
            Eye_Ratio = (left_Eye+right_Eye)/2

            # round average eyeratio to 2 decimal points
            Eye_Ratio = round(Eye_Ratio, 2)

            # if eye ratio lower than 0.2 for 5 continuous cycles then designate as fatigue
            if Eye_Ratio < 0.2:
                count += 1
            else:
                window.update("Great Job! You appear to be calm and alert \nfor the drive ahead. ")
                count = 0
            if count >= 5:
                instances += 1
                window.update("It seems like you might be fatigued. It's \nessential to stay alert on the road. If you're feeling\ntired, please consider taking a break or grabbing\n a coffee to recharge before continuing. ")

        #display frame
        frame = cv2.resize(frame, (720, 500))
        cv2.namedWindow("Video Camera")
        cv2.moveWindow("Video Camera", 720, 0)
        cv2.imshow("Video Camera", frame)
        key = cv2.waitKey(9)
        if key == 20:
            break

    cap.release()
    cv2.destroyAllWindows()

    return instances


