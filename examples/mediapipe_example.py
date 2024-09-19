import cv2 as cv
import mediapipe as mp
import numpy as np
import time
from typing import Tuple


# Sets the camera dimensions to have width of 640px and scales it to the camera aspect ratio of the device
def setCameraDimensions(capture: cv.VideoCapture) -> Tuple[int, int]:
    frame  = capture.read()[1]

    width = 640
    height = int(frame.shape[0] * width / frame.shape[1])

    return (width, height)

def displayFPS(image: cv.UMat, presentTime: float) -> Tuple[cv.UMat, float]:
    currentTime = time.time()
    fps = 1/(currentTime-presentTime)
    presentTime = currentTime

    image = cv.putText(image, f"FPS: {str(int(fps))}", (10,70), cv.FONT_HERSHEY_PLAIN, 1, color=(255,255,255), thickness=2)

    return image, presentTime

if __name__ == "__main__":
    
    # Initialize capture   
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        raise RuntimeError("Failed to open camera.")
    
    

    # Initialize dimensions
    width, height = setCameraDimensions(capture)

    

    # Initializes Mediapipe
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    # Initialization for displaying FPS
    presentTime = 0

    while True:

        
        # Reads the current frame
        isTrue, initialImg = capture.read() 
        img = cv.flip(cv.resize(initialImg, (width, height)),1)
        
        # Creates a blank frame
        blank = np.zeros((height, width, 3), dtype='uint8')

        # Gets hand objects if they are present in the screen
        results = hands.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:

            for handLandmarks in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(blank, handLandmarks, mpHands.HAND_CONNECTIONS)



        # Displays FPS
        blank, presentTime = displayFPS(blank, presentTime)

        # Displays the image in a window 'Video'
        cv.imshow('Hand Tracking', blank)
        cv.imshow('Video ', img)

        # Press d to exit
        if cv.waitKey(1) &  0xFF==ord('d'):
            break

    capture.release()
    cv.destroyAllWindows()