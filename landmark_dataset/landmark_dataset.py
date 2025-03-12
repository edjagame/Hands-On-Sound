import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import os
import logging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
file_handler = logging.FileHandler('output.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


# Load mediapipe hands module and create hands object
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Function to get hand landmarks from the image
def get_landmarks(image):
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

    gesture_names = {'flute': 0, 'generic': 1, 'snareDrum': 2, 'trumpet': 3, 'violin': 4}

    # Initialize lists to store landmarks and labels
    # landmarks are the actual 62 coordinates of the hand (21 lms * 3 coords)
    # labels correspond to which gesture the landmarks belong to
    landmarks = []
    labels = []
    
    # Load image from resources folder
    # For each image in the folder, get the landmarks and append them to the landmarks list,
    # then append the corresponding label to the labels list
    for gesture in gesture_names:
        folder_path = f'resources\\training_data\\{gesture}'
        for file_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, file_name)
            logger.info(f"Processing {image_path}")
            image = cv.imread(image_path)
            if image is None:
                logger.error(f"Error: Unable to load image at {image_path}")
                exit()
            
            lms = get_landmarks(image)
            if len(lms) == 21:
                landmarks.append(lms)
                labels.append(gesture_names[gesture])
            else:
                logger.warning(f"Found {len(lms)} landmarks at {image_path}.")

    
    # Convert lists to numpy arrays and save them to a file
    landmarks = np.array(landmarks)
    labels = np.array(labels)
    np.save('landmarks.npy', landmarks)
    np.save('labels.npy', labels)

    cv.destroyAllWindows()      