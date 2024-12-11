import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

import images

# measurements of Video
height, width = 2110, 2110

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

folderPath = 'Presentation/DP'

pathImages = sorted(images.l)
#pathImages = sorted(os.listdir(folderPath), key=len)  # list

#Number of Slides
imgNum = 0

#Measurement of Small Video on Slides
hs, ws = int(120), int(213)

#Measurement of Slides
hi, wi = 720, 1280

#Controlling Slides
buttonPressed = False
buttonCounter = 0
buttonDelay = 30

#Drawing Seprately
annotations = [[]]
annotationsNum = 0
annotationsStart = False

detector = HandDetector(detectionCon=0.8, maxHands=1)

gestureThreshold = 300

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = pathImages[imgNum]  #os.path.join(folderPath, pathImages[imgNum])
    imgg = cv2.imread(pathFullImage)
    imgCurrent = cv2.resize(imgg, (wi, hi))

    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)
    #cv2.line(img, (300, 0), (300, height), (0, 255, 0), 3)
    #cv2.line(img, (600, 0), (600, height), (0, 255, 0), 3)
    #cv2.line(img, (0, 50), (width, 50), (0, 255, 0), 3)
    #cv2.line(img, (0, 450), (width, 450), (0, 255, 0), 3)

    hands, img = detector.findHands(img)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        cx, cy = hand['center']

        lmList = hand['lmList']
        #indexFinger = lmList[8][0], lmList[8][1]

        x = int(np.interp(lmList[8][0], [width//3, wi], [0, width]))
        y = int(np.interp(lmList[8][1], [1, height-1], [0, height-1]))

        indexFinger = x, y

        if cy <= gestureThreshold:

            # Gesture - 1 Left
            if fingers == [1, 0, 0, 0, 0]:
                print('Left')
                if imgNum >= 1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationsNum = 0
                    annotationsStart = False

                    imgNum -= 1

            # Gesture - 2 Right
            if fingers == [0, 0, 0, 0, 1]:
                print('Right')
                if imgNum < len(pathImages) - 1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationsNum = 0
                    annotationsStart = False

                    imgNum += 1

        #if cx >= 300 and cx <= 600:

        # Gesture - 3 Pointer
        if fingers == [0, 1, 1, 0, 0]:
                # print('Pointer')
            cv2.circle(imgCurrent, indexFinger, 12, (0,0,255), cv2.FILLED)

        #Gesture - 4 Draw
        if fingers == [0, 1, 0, 0, 0]:
            if annotationsStart is False:
                annotationsStart = True
                annotationsNum += 1
                annotations.append([])

            cv2.circle(imgCurrent, indexFinger, 8, (0, 0, 255), cv2.FILLED)
            annotations[annotationsNum].append(indexFinger)

        else:
            annotationsStart = False

        #Gesture - 5 Erase
        if fingers == [0, 1, 1, 1, 0]:
            #print('Delete')
            if annotations:
                if annotationsNum >= 0:

                    annotations.pop(-1)
                    annotationsNum -= 1
                    buttonPressed = True

    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent, annotations[i][j-1], annotations[i][j], (0,0,200), 8)



    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws:w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow('Slide', imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
