import time
from typing import Tuple

import tkinter as tk
from tkinter import ttk

import cv2 as cv
import mediapipe as mp
import numpy as np
from keras.models import load_model

from hands_on_sound.paths import ACTIVE_MODEL_PATH
from hands_on_sound.sound_player import SoundPlayer

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 960
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)


# Derive a display size that preserves the camera aspect ratio.
def setCameraDimensions(capture: cv.VideoCapture) -> Tuple[int, int]:
    frame  = capture.read()[1]

    width = CAMERA_WIDTH
    height = int(frame.shape[0] * width / frame.shape[1])

    return (width, height)


# Overlay the current frame rate for debugging.
def displayFPS(image: cv.UMat, present_time: float) -> Tuple[cv.UMat, float]:
    currentTime = time.time()
    fps = 1/(currentTime-present_time)
    present_time = currentTime

    image = cv.putText(image, f"FPS: {str(int(fps))}", (10,70), cv.FONT_HERSHEY_PLAIN, 1, color=(255,255,255), thickness=2)

    return image, present_time


# Extract landmarks and mirror left-hand coordinates so both hands match the training data.
def get_landmarks(image) -> list:
    hand_data = []
    results = hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    if results.multi_hand_landmarks: 
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            lms = []
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
            hand_data.append((lms, handedness.classification[0].label))
    return hand_data


# Map landmark predictions back to instrument labels.
def predict_gesture(hand_lms: list) -> Tuple[str, float]:
    prediction = model.predict(np.array([hand_lms]))
    gesture_id = np.argmax(prediction)
    gesture = ['flute', 'generic', 'snareDrum', 'trumpet', 'violin'][gesture_id]
    confidence = np.max(prediction)
    return gesture, confidence

def settings():
    root = tk.Tk()
    root.title("Hands-On Sound Settings")
    frm = ttk.Frame(root, padding=30)
    frm.grid()

    ttk.Label(frm, text="Key").grid(column=0, row=0)
    key = tk.StringVar(value="C")
    key_dropdown = ttk.Combobox(
        frm, textvariable=key, values=["C", "D", "E", "G", "A", "B", "F#", "C#", "Ab", "Eb", "Bb", "F"]
    )
    key_dropdown.grid(column=1, row=0)

    mode = tk.StringVar(value="major")
    major_radio = ttk.Radiobutton(
        frm, text="Major", variable=mode, value="major"
    ).grid(column=0, row=2)
    minor_radio = ttk.Radiobutton(
        frm, text="Minor", variable=mode, value="minor"
    ).grid(column=1, row=2)

    settings = {}
    def confirm():
        settings['key'] = key.get()
        settings['mode'] = mode.get()
        root.destroy()

    ttk.Button(frm, text="Confirm", command=confirm).grid(column=0, row=3)
    root.mainloop()
    return settings['key'], settings['mode']

def main():
    global model, mp_hands, hands, mp_draw

    selected_settings = settings()

    # Load the gesture prediction model selected by the app.
    model = load_model(str(ACTIVE_MODEL_PATH))

    # Initialize MediaPipe hand tracking.
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_draw = mp.solutions.drawing_utils

    # Open the default camera feed.
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        raise RuntimeError("Failed to open camera.")
    
    # Compute the render size once so the display stays consistent.
    width, height = setCameraDimensions(capture)

    scale_index = 0
    mode_index = 0

    # Load instrument samples for the selected key and mode.
    sp = SoundPlayer()
    sp.set_scale(selected_settings[0], selected_settings[1])
    
    present_time = 0
    current_frame = 0
    idle_frames = [0,0]
    prediction_frequency = 1
    current_predictions = [None, None]
    center_x_list = [None, None]
    center_y_list = [None, None]

    previous_sounds = [None, None]
    current_sounds = [None, None]
    current_notes = [None, None]

    while True:
        # Read and normalize the current frame.
        isTrue, initial_img = capture.read() 
        img = cv.flip(cv.resize(initial_img, (width, height)),1)
        black_img = np.zeros((height, width, 3), np.uint8)

        # Draw the note guide for each column on the screen.
        for j in range(12):
            cv.line(black_img, (int(j * width / 12), 0), (int(j * width / 12), height), WHITE, 1)
            cv.putText(black_img, sp.get_note_names(sp.scale, sp.mode)[j % 7], (int(j * width / 12) + 50, 100), cv.FONT_HERSHEY_PLAIN, 2, WHITE, thickness=2)
            match j % 4:
                case 0:
                    cv.putText(black_img, 'eighth', (int(j * width / 12) + 10, height-200), cv.FONT_HERSHEY_PLAIN, 1, WHITE, thickness=2)
                case 1:
                    cv.putText(black_img, 'quarter', (int(j * width / 12) + 10, height-200), cv.FONT_HERSHEY_PLAIN, 1, WHITE, thickness=2)
                case 2:
                    cv.putText(black_img, 'half', (int(j * width / 12) + 10, height-200), cv.FONT_HERSHEY_PLAIN, 1, WHITE, thickness=2)
                case 3:
                    cv.putText(black_img, 'whole', (int(j * width / 12) + 10, height-200), cv.FONT_HERSHEY_PLAIN, 1, WHITE, thickness=2)
        cv.putText(black_img, f'Key: {sp.scale}', (width - 200, 30), cv.FONT_HERSHEY_PLAIN, 2, WHITE, thickness=1)
        cv.putText(black_img, f'Mode: {sp.mode}', (width - 200, 60), cv.FONT_HERSHEY_PLAIN, 2, WHITE, thickness=1)
        
        # Refresh gesture predictions every few frames to reduce inference cost.
        if current_frame % prediction_frequency == 0:
            hand_data = get_landmarks(img)
            if current_predictions:
                current_predictions = [None, None]
            if hand_data:
                for i, hand in enumerate(hand_data):
                    lms = hand[0]
                    handedness = hand[1]
                    gesture, confidence = predict_gesture(lms)
                    center_x = int(lms[9][0] * CAMERA_WIDTH) if handedness == 'Right' else int((1-lms[9][0]) * CAMERA_WIDTH)
                    center_y = int(lms[9][1] * CAMERA_HEIGHT)
                    if handedness == 'Left':
                        current_predictions[0] = (gesture, confidence, center_x, center_y, 0)
                    elif handedness == 'Right':
                        current_predictions[1] = (gesture, confidence, center_x, center_y, 1)

        # Convert the latest gesture predictions into active sounds.
        if current_predictions:
            for i, prediction in enumerate(current_predictions):
                if prediction:
                    gesture = prediction[0]
                    confidence = prediction[1]
                    center_x_list[0 if prediction[4] == 0 else 1] = prediction[2]
                    center_y_list[0 if prediction[4] == 0 else 1] = prediction[3]
                    sp.current_sounds[i] = sp.sounds[gesture]
                    sp.set_volume(sp.channels[i], center_y_list[i], height)
                    cv.putText(black_img, f'{"Left" if i == 0 else "Right"} Hand: {gesture if gesture != "generic" else "rest"}', (20, 30 * (i+1)), cv.FONT_HERSHEY_PLAIN, 3, (255-i*128,128,128+i*128), thickness=2)   
                    idle_frames[i] = 0

        # Keep each hand mapped to a note until it leaves the active area.
        for i in range(2):
            if idle_frames[i] < prediction_frequency * 5:
                # Draw the detected hand position and play the matching note.
                if center_x_list[i] and center_y_list[i]:
                    if i == 0:
                        cv.circle(black_img, (center_x_list[i], center_y_list[i]), 10, (255,128,128), cv.FILLED)
                    if i == 1:
                        cv.circle(black_img, (center_x_list[i], center_y_list[i]), 10, (128,128,255), cv.FILLED)
                    new_note = sp.get_note(center_x_list[i], width, sp.current_sounds[i])

                    if new_note != current_notes[i] or previous_sounds[i] != sp.current_sounds[i]:
                        if current_notes[i]:
                            sp.stop_sound(sp.channels[i])
                        if new_note:
                            sp.play_sound(new_note, sp.channels[i])
                            current_notes[i] = new_note
                        previous_sounds[i] = sp.current_sounds[i]
            else:
                sp.stop_sound(sp.channels[i])
                    
        # Show the processed frame and the original camera feed.
        cv.imshow('Hand Gesture Recognition', black_img)
        cv.imshow('Original', cv.resize(img, (320, 240)))

        current_frame += 1
        idle_frames[0] += 1

        idle_frames[1] += 1
        
        # Keyboard input.
        key = cv.waitKey(1) & 0xFF

        # Press q or Esc to exit.
        if key == ord('q') or key == 27:
            break
    
    capture.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
