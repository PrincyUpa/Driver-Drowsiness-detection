# Program for eye and yawn detection
from django.shortcuts import render
import time
import cv2
import dlib
import threading
from imutils import face_utils
from scipy.spatial import distance as dist
import pygame


# Eye Aspect Ratio Calculation
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


# Mouth Aspect Ratio Calculation
def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[13], mouth[19])
    B = dist.euclidean(mouth[14], mouth[18])
    C = dist.euclidean(mouth[15], mouth[17])

    MAR = (A + B + C) / 3.0
    return MAR


# Loading sound alarm
def sound_alarm():
    pygame.mixer.init()
    pygame.mixer.music.load("sound files_alarm.mp3")
    pygame.mixer.music.play()


# Starting the application
def start(request):
    MAR_THRESHOLD = 14
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 30

    COUNTER_EYE = 0
    COUNTER_YAWN = 0
    TOTAL_EYE = 0
    TOTAL_YAWN = 0

    ALARM_ON = False

    videoSteam = cv2.VideoCapture(0)
    ret, frame = videoSteam.read()
    size = frame.shape

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mstart, mend) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

    t_end = time.time()

    while True:

        ret, frame = videoSteam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)

        for rect in rects:

            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            mouth = shape[mstart:mend]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            ear = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)

            MAR = mouth_aspect_ratio(mouth)
            cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (255, 255, 0), 1)
            cv2.drawContours(frame, [mouth], -1, (255, 255, 0), 1)

            # Count number of blinks
            if ear < EYE_AR_THRESH:
                COUNTER_EYE += 1
                # If eye reamin close for 90 or more consecutive frames i.e. for approx. 5 seconds or more then alert signal is sent
                if COUNTER_EYE >= 3 * EYE_AR_CONSEC_FRAMES:
                    if not ALARM_ON:
                        ALARM_ON = True
                        d = threading.Thread(target=sound_alarm)
                        d.setDaemon(True)
                        d.start()
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord("s"):
                            if ALARM_ON:
                                pygame.mixer.music.quit()
                    cv2.putText(frame, "Send Alert!", (200, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)
            else:
                if COUNTER_EYE >= EYE_AR_CONSEC_FRAMES:
                    TOTAL_EYE += 1

                COUNTER_EYE = 0

            # Count number of yawn
            if MAR > MAR_THRESHOLD:
                COUNTER_YAWN += 1
                cv2.drawContours(frame, [mouth], -1, (255, 255, 0), 1)
            else:
                if COUNTER_YAWN >= EYE_AR_CONSEC_FRAMES:
                    TOTAL_YAWN += 1

                COUNTER_YAWN = 0

            # Condition to detect drowsiness based on number of blinks and number of yawn
            if TOTAL_EYE >= 2 and TOTAL_YAWN >= 1:
                if not ALARM_ON:
                    ALARM_ON = True
                    d = threading.Thread(target=sound_alarm)
                    d.setDaemon(True)
                    d.start()
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("s"):
                        if ALARM_ON:
                            pygame.mixer.music.quit()
                cv2.putText(frame, "Send Alert!", (200, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)

            # Condition to detect drowsiness based on number of blinks
            elif TOTAL_EYE >= 3:
                if not ALARM_ON:
                    ALARM_ON = True
                    d = threading.Thread(target=sound_alarm)
                    d.setDaemon(True)
                    d.start()
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("s"):
                        if ALARM_ON:
                            pygame.mixer.music.quit()
                cv2.putText(frame, "Send Alert!", (200, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)

            # Condition to detect drowsiness based on number of yawn
            elif TOTAL_YAWN >= 2:
                if not ALARM_ON:
                    ALARM_ON = True
                    d = threading.Thread(target=sound_alarm)
                    d.setDaemon(True)
                    d.start()
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("s"):
                        if ALARM_ON:
                            pygame.mixer.music.quit()
                cv2.putText(frame, "Send Alert!", (200, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)

            cv2.putText(
                frame,
                "Blinks: {}".format(TOTAL_EYE),
                (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            cv2.putText(
                frame,
                "EAR: {:.2f}".format(ear),
                (30, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            cv2.putText(
                frame,
                "Yawn: {}".format(TOTAL_YAWN),
                (430, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            cv2.putText(
                frame,
                "MAR: {:.2f}".format(MAR),
                (430, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            cv2.putText(frame, "Press q for exit", (30, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    videoSteam.release()

    return render(request, 'index.html')
