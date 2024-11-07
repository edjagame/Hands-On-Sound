import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import logging
from typing import Tuple
from keras.models import load_model

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
model = load_model('hand_gesture_instrument_model.keras')

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

    width = CAMERA_WIDTH
    height = int(frame.shape[0] * width / frame.shape[1])

    return (width, height)

def displayFPS(image: cv.UMat, presentTime: float) -> Tuple[cv.UMat, float]:
    currentTime = time.time()
    fps = 1/(currentTime-presentTime)
    presentTime = currentTime

    image = cv.putText(image, f"FPS: {str(int(fps))}", (10,70), cv.FONT_HERSHEY_PLAIN, 1, color=(255,255,255), thickness=2)

    return image, presentTime

# Function to get hand landmarks from the image
# Slightly different from model_creation.py and landmark_dataset.py
def get_landmarks(image) -> list:
    hand_data = []
    # Processes visible hand objects in the screen
    results = hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    if results.multi_hand_landmarks: 
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            lms = []
            # Draws the landmarks on the image
            # mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            for id, lm in enumerate(hand_landmarks.landmark):
                lm_coords = []
                # The training data was using right hand, so we mirror the left hand landmarks to match the right hand
                if handedness.classification[0].label == 'Left':
                    lm_coords.append(1-lm.x)
                else:
                    lm_coords.append(lm.x)
                lm_coords.append(lm.y)
                lm_coords.append(lm.z)
                if len(lm_coords) == 3:
                    lms.append(lm_coords)
                else:
                    logger.warning(f"Found {len(lm_coords)} coordinates (expected 3).")
            hand_data.append((lms, handedness.classification[0].label))
    return hand_data

def get_hand_center(hand):
    palm_landmarks = [0, 5, 6, 9, 10, 13, 14, 17, 18]
    center_x = int(np.mean([hand[i][0] for i in palm_landmarks]) * CAMERA_WIDTH)
    center_y = int(np.mean([hand[i][1] for i in palm_landmarks]) * CAMERA_HEIGHT)
    return center_x, center_y

def predict_gesture(hand_lms: list) -> Tuple[str, float]:
    prediction = model.predict(np.array([hand_lms]))
    gesture_id = np.argmax(prediction)
    gesture = ['flute', 'generic', 'snareDrum', 'trumpet', 'violin'][gesture_id]
    confidence = np.max(prediction)
    return gesture, confidence

if __name__ == "__main__":
    # Initialize capture   
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        raise RuntimeError("Failed to open camera.")
    
    # Initialize dimensions
    width, height = setCameraDimensions(capture)

    # Initialization for displaying FPS
    presentTime = 0
    currentFrame = 0
    predictionFrequency = 3

    last_predictions = []
    while True:
        # Reads the current frame
        isTrue, initialImg = capture.read() 
        img = cv.flip(cv.resize(initialImg, (width, height)),1)
        black_img = np.zeros((height, width, 3), np.uint8)
        # hand_lms returns a list of landmarks for each hand in the image
        if currentFrame % predictionFrequency == 0:
            hand_data = get_landmarks(img)
            
            last_predictions.clear()
            if hand_data:
                for i, hand in enumerate(hand_data):
                    lms = hand[0]
                    handedness = hand[1]
                    gesture, confidence = predict_gesture(lms)
                    # center_x, center_y = get_hand_center(lms)
                    center_x = int(lms[9][0] * CAMERA_WIDTH) if handedness == 'Right' else int((1-lms[9][0]) * CAMERA_WIDTH)
                    center_y = int(lms[9][1] * CAMERA_HEIGHT)
                    last_predictions.append((gesture, confidence, center_x, center_y))

        if last_predictions:
            for i, prediction in enumerate(last_predictions):
                gesture = prediction[0]
                confidence = prediction[1]
                center_x = prediction[2]
                center_y = prediction[3]
                cv.putText(black_img, f'Hand {i+1}: {gesture} ({confidence*100:.2f}%)', (20, 30 * (i+1)), cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness=2)   
                cv.circle(black_img, (center_x, center_y), 5, (0,255,0), cv.FILLED)     

        # Display FPS
        black_img, presentTime = displayFPS(black_img, presentTime)
        cv.imshow('Hand Gesture Recognition', black_img)
        cv.imshow('Original', img)
        currentFrame += 1

        # Press d to exit
        if cv.waitKey(1) &  0xFF==ord('d'):
            break
    
    capture.release()
    cv.destroyAllWindows()