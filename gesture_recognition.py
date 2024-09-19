import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import logging
from typing import Tuple
from keras.models import load_model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
file_handler = logging.FileHandler('gr_output.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


# Initializes Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

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

# Function to get hand landmarks from the image
def get_landmarks(image) -> list:
    lms = []
    # Processes visible hand objects in the screen
    results = hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    if results.multi_hand_landmarks: 
        for handLandmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, handLandmarks, mp_hands.HAND_CONNECTIONS)
            for id, lm in enumerate(handLandmarks.landmark):
                lm_coords = []
                lm_coords.append(lm.x)
                lm_coords.append(lm.y)
                lm_coords.append(lm.z)
                if len(lm_coords) == 3:
                    lms.append(lm_coords)
                else:
                    logger.warning(f"Found {len(lm_coords)} coordinates (expected 3).")
    return lms

if __name__ == "__main__":
    
    # Load the model
    model = load_model('hand_gesture_instrument_model.keras')

    # Initialize capture   
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        raise RuntimeError("Failed to open camera.")
    
    # Initialize dimensions
    width, height = setCameraDimensions(capture)

    # Initialization for displaying FPS
    presentTime = 0

    while True:

        # Reads the current frame
        isTrue, initialImg = capture.read() 
        img = cv.flip(cv.resize(initialImg, (width, height)),1)
    
        lms = get_landmarks(img)
        if len(lms)==21:
            prediction = model.predict(np.array([lms]))
            gesture_id = np.argmax(prediction)
            gesture = ['flute', 'generic', 'snareDrum', 'trumpet', 'violin'][gesture_id]
            confidence = np.max(prediction)
            cv.putText(img, f'Gesture: {gesture} ({confidence}%)', (20,20), cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness=3)

        cv.imshow('Video', img)

        # Press d to exit
        if cv.waitKey(20) &  0xFF==ord('d'):
            break

    capture.release()
    cv.destroyAllWindows()