import os
import cv2
import time  # Import the time module
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from legacy.hands_on_sound.paths import IMAGE_DATA_DIR

DATA_DIR = IMAGE_DATA_DIR
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 5
dataset_size = 1000  # change this to the number you wanna end with (not inclusive)

# cap = cv2.VideoCapture(2)
cap = cv2.VideoCapture(0)

for j in range(number_of_classes):
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print('Collecting data for class {}'.format(j))

    done = False
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    time.sleep(1)  # Add a delay of 1 second before starting to capture images
    counter = 800  # change this to the number you wanna start with
    while counter < dataset_size:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

        counter += 1
        time.sleep(0.2)  # Add a delay of 1 second between each picture

cap.release()
cv2.destroyAllWindows()


# import os

# import cv2

# # new
# import time

# DATA_DIR = './data'
# if not os.path.exists(DATA_DIR):
#     os.makedirs(DATA_DIR)

# number_of_classes = 5
# dataset_size = 200 #change this to the number you wanna end with (not inclusive)

# # cap = cv2.VideoCapture(2)
# cap = cv2.VideoCapture(0)

# # new 
# # while True:
# #     ret, frame = cap.read()  # Capture frame
# #     if not ret:  # Check if frame was captured
# #         print("Failed to capture frame")
# #         break  # Exit loop or continue based on your needs
    
# #     # Now safe to show the frame
# #     cv2.imshow('frame', frame)

# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # cap.release()
# # cv2.destroyAllWindows()

# for j in range(number_of_classes):
#     if not os.path.exists(os.path.join(DATA_DIR, str(j))):
#         os.makedirs(os.path.join(DATA_DIR, str(j)))

#     print('Collecting data for class {}'.format(j))

#     done = False
#     while True:
#         ret, frame = cap.read()
#         cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
#                     cv2.LINE_AA)
#         cv2.imshow('frame', frame)
#         if cv2.waitKey(25) == ord('q'):
#             break

#     counter = 0 # change this to the number you wanna start with
#     # counter = 0
#     while counter < dataset_size:
#         ret, frame = cap.read()
#         cv2.imshow('frame', frame)
#         cv2.waitKey(25)
#         cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

#         counter += 1

# cap.release()
# cv2.destroyAllWindows()
