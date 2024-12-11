import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

height, width = 1280, 720


cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)


    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)


        # Gesture - 1 Left
        if fingers == [1, 0, 0, 0, 0]:
            print('Left')

        # Gesture - 2 Right
        if fingers == [0, 0, 0, 0, 1]:
            print('Right')

        # Gesture - 3 Pointer
        if fingers == [0, 1, 0, 0, 0]:
            print('Draw')

        # Gesture - 4 Draw
        if fingers == [0, 1, 1, 0, 0]:
            print('Pointer')

        # Gesture - 5 Erase
        if fingers == [0, 1, 1, 1, 0]:
            print('Delete')


    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
