import numpy as np
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Load the data obtained in landmark_dataset/
landmarks = np.load('landmark_dataset/landmarks.npy')
labels = np.load('landmark_dataset/labels.npy')

# Print shapes to verify
print(f"Original Landmarks shape: {landmarks.shape}")
print(f"Original Labels shape: {labels.shape}")

# Ensure landmarks are 2D and reshape to add a channel dimension
# Assuming landmarks have shape (num_samples, height, width)
# If landmarks are 1D, reshape them accordingly
if len(landmarks.shape) == 2:
    landmarks = landmarks.reshape(landmarks.shape[0], landmarks.shape[1], 1, 1)
elif len(landmarks.shape) == 3:
    landmarks = landmarks.reshape(landmarks.shape[0], landmarks.shape[1], landmarks.shape[2], 1)

# Print new shape to verify
print(f"Reshaped Landmarks shape: {landmarks.shape}")