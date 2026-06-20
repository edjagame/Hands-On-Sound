import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import logging
from pathlib import Path
import sys
from typing import Tuple
from keras.models import load_model

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hands_on_sound.paths import ACTIVE_MODEL_PATH, IMAGE_DATA_DIR, LOGS_DIR

# Configure logging
LOGS_DIR.mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
file_handler = logging.FileHandler(LOGS_DIR / 'test_images_output.log')
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

def predict_gesture(img: cv.UMat) -> cv.UMat:
    hand_lms = get_landmarks(img)
    for i, hand in enumerate(hand_lms):
        prediction = model.predict(np.array([hand]))
        gesture_id = np.argmax(prediction)
        gesture = ['flute', 'generic', 'snareDrum', 'trumpet', 'violin'][gesture_id]
        confidence = np.max(prediction)
        cv.putText(img, f'Hand {i+1}: {gesture} ({confidence*100:.2f}%)', (20, 30 * (i+1)), cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness=3)
    return img
# Function to get hand landmarks from the image
# Slightly different from train_model.py and data/create_landmark_dataset.py
def get_landmarks(image) -> list:
    hand_lms = []
    # Processes visible hand objects in the screen
    results = hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    if results.multi_hand_landmarks: 
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            lms = []
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            for id, lm in enumerate(hand_landmarks.landmark):
                lm_coords = []
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
            hand_lms.append(lms)
    return hand_lms

if __name__ == "__main__":
    
    # Load the model
    model = load_model(str(ACTIVE_MODEL_PATH))

    # Initialize capture   
    image_path = IMAGE_DATA_DIR / '0' / '600.jpg'
    image = cv.imread(str(image_path))
    flipped = cv.flip(image, 1)
    image = predict_gesture(image)
    flipped = predict_gesture(flipped)

    cv.imshow(f'Image', image)
    cv.imshow(f'Flipped Image', flipped)

    # Press d to exit
    cv.waitKey(0)
    cv.destroyAllWindows()
