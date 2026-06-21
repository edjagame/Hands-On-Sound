import cv2 as cv
import mediapipe as mp
import numpy as np

from typing import Tuple

import pygame

import threading
import time
import logging
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from legacy.hands_on_sound.paths import ACTIVE_MODEL_PATH, SOUNDS_DIR

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


# Sets the camera dimensions to have width of 640px and scales it to the camera aspect ratio of the device
def setCameraDimensions(capture: cv.VideoCapture) -> Tuple[int, int]:
    frame  = capture.read()[1]

    width = CAMERA_WIDTH
    height = int(frame.shape[0] * width / frame.shape[1])

    return (width, height)

# Function to display the FPS on screen
def displayFPS(image: cv.UMat, present_time: float) -> Tuple[cv.UMat, float]:
    currentTime = time.time()
    fps = 1/(currentTime-present_time)
    present_time = currentTime

    image = cv.putText(image, f"FPS: {str(int(fps))}", (10,70), cv.FONT_HERSHEY_PLAIN, 1, color=(255,255,255), thickness=2)

    return image, present_time

# Function to get hand landmarks from the image
def get_landmarks(image) -> list:
    hand_data = []
    # Processes visible hand objects in the screen
    results = hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    if results.multi_hand_landmarks: 
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            lms = []
            # Draws the landmarks on the image
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
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
            hand_data.append((lms, handedness.classification[0].label))
    return hand_data

# Function to predict the hand gesture based on hand landmarks
def predict_gesture(hand_lms: list) -> Tuple[str, float]:
    prediction = model.predict(np.array([hand_lms]))
    gesture_id = np.argmax(prediction)
    gesture = ['flute', 'generic', 'snareDrum', 'trumpet', 'violin'][gesture_id]
    confidence = np.max(prediction)
    return gesture, confidence

#Function to load the sounds based on the instrument
notes = ["A3", "B3", "C#4", "D4", "E4", "F#4", "G#4", "A4", "B4", "C#5", "D5", "E5", "F#5", "G#5", "A5"]
sounds_folder = SOUNDS_DIR
def load_sounds(instrument):
    folder = os.path.join(sounds_folder, instrument)
    sounds = {}
    for note in notes:
        path = os.path.join(folder, note + ".wav")
        if os.path.exists(path):
            sounds[note] = pygame.mixer.Sound(path)
        else:
            print(f"File not found: {path}")
    return sounds

def play_sound(note, sounds, channel):
    if note in sounds:
        channel.play(sounds[note], loops=-1, fade_ms=100)

def stop_sound(channel):
        channel.fadeout(500)

def get_note(center_x, width):
    note_index = int(center_x / (width / len(notes)))
    return notes[min(note_index, len(notes) - 1)]   

if __name__ == "__main__":
    #Loads the gesture prediciton model
    model = load_model(str(ACTIVE_MODEL_PATH))

    # Initializes Mediapipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    # Initialize capture   
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        raise RuntimeError("Failed to open camera.")
    
    # Initialize dimensions
    width, height = setCameraDimensions(capture)

    # Load the mixer and sounds
    pygame.mixer.init()
    channels = {0: pygame.mixer.Channel(0), 1: pygame.mixer.Channel(1)}

    violin_sounds = load_sounds("violin")
    flute_sounds = load_sounds("flute")
    snare_sounds = load_sounds("snare")
    trumpet_sounds = load_sounds("trumpet")
    generic_sounds = load_sounds("generic")

    # Some initial variables
    # present_time is used to calculate the FPS
    # current_frame is used to keep track of the current frame
    # idle_frames is used to keep track of the number of frames the program has not detected any hand gestures
    # prediction_frequency is used to determine how often the program should predict the hand gesture
    # previous_predictions and current_predictions are used to keep track of the previous and current predictions

    present_time = 0
    current_frame = 0
    idle_frames = [0,0]
    prediction_frequency = 3
    previous_predictions = [None, None]
    current_predictions = [None, None]
    center_x_list = [None, None]
    center_y_list = [None, None]
    current_notes = [None, None]

    while True:
        # Reads the current frame
        isTrue, initial_img = capture.read() 
        img = cv.flip(cv.resize(initial_img, (width, height)),1)
        black_img = np.zeros((height, width, 3), np.uint8)

        # Get hand landmarks, happens every prediction_frequency frames
        if current_frame % prediction_frequency == 0:
            hand_data = get_landmarks(img)
            if current_predictions:
                previous_predictions = [None, None]
                previous_predictions = current_predictions.copy()
                current_predictions = [None, None]
            if hand_data:
                for i, hand in enumerate(hand_data):
                    lms = hand[0]
                    handedness = hand[1]
                    gesture, confidence = predict_gesture(lms)
                    # center_x, center_y = get_hand_center(lms)
                    center_x = int(lms[9][0] * CAMERA_WIDTH) if handedness == 'Right' else int((1-lms[9][0]) * CAMERA_WIDTH)
                    center_y = int(lms[9][1] * CAMERA_HEIGHT)
                    if handedness == 'Left':
                        current_predictions[0] = (gesture, confidence, center_x, center_y, 0)
                    elif handedness == 'Right':
                        current_predictions[1] = (gesture, confidence, center_x, center_y, 1)

        # Display the hand gesture prediction
        if current_predictions:
            for i, prediction in enumerate(current_predictions):
                if prediction:
                    gesture = prediction[0]
                    confidence = prediction[1]
                    center_x_list[0 if prediction[4] == 0 else 1] = prediction[2]
                    center_y_list[0 if prediction[4] == 0 else 1] = prediction[3]
                    cv.putText(black_img, f'Hand {i+1}: {gesture} ({confidence*100:.2f}%)', (20, 30 * (i+1)), cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), thickness=2)   
                    idle_frames[i] = 0
                    
        # # Get the note based on the x position of the hand
        # note_index = int(center_x_list[i] / (CAMERA_WIDTH / len(notes)))
        # note = notes[min(note_index, len(notes) - 1)]

        for i in range(2):
            if idle_frames[i] < prediction_frequency * 5:
            # Draw the center of the hand on the screen
                if center_x_list[i] and center_y_list[i]:
                    cv.circle(black_img, (center_x_list[i], center_y_list[i]), 10, (0,255,0), cv.FILLED)
                    # Play the sound
                    new_note = get_note(center_x_list[i], width)
                    if new_note != current_notes[i]:
                        if current_notes[i]:
                            stop_sound(channels[i])

                        play_sound(new_note, violin_sounds, channels[i])
                        current_notes[i] = new_note
            else:
                stop_sound(channels[i])
                    
        # Display FPS
        black_img, present_time = displayFPS(black_img, present_time)

        # Display the captures
        cv.imshow('Hand Gesture Recognition', black_img)
        cv.imshow('Original', img)

        current_frame += 1
        idle_frames[0] += 1
        idle_frames[1] += 1

        # Press d to exit
        if cv.waitKey(1) &  0xFF==ord('d'):
            break
    
    capture.release()
    cv.destroyAllWindows()
