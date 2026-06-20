import numpy as np
from pathlib import Path
import sys

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hands_on_sound.paths import ACTIVE_MODEL_PATH, LABELS_PATH, LANDMARKS_PATH

# Load the landmark dataset generated from the collected images.
landmarks = np.load(LANDMARKS_PATH)
labels = np.load(LABELS_PATH)

# Reshape landmarks into the format expected by the 1D convolution layers.
landmarks = landmarks.reshape(landmarks.shape[0], landmarks.shape[1], landmarks.shape[2])

# Convert integer labels to one-hot encoded vectors.
num_classes = len(np.unique(labels))
labels = to_categorical(labels, num_classes=num_classes)

# Split the data into training and validation sets.
X_train, X_test, y_train, y_test = train_test_split(landmarks, labels, test_size=0.15, random_state=9999)

# Define the gesture classifier.
model = Sequential([
    Conv1D(filters=32, kernel_size=3, activation='relu', input_shape=(landmarks.shape[1], landmarks.shape[2])),
    MaxPooling1D(pool_size=2),
    Conv1D(64, kernel_size=3, activation='relu'),
    MaxPooling1D(pool_size=2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

model.summary()

# Compile and train the model.
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=35, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the trained model on the held-out validation set.
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# Save the trained model for the runtime app.
model.save(str(ACTIVE_MODEL_PATH))
