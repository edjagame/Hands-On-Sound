import numpy as np

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout



# Load the data obtained in landmark_dataset/
landmarks = np.load('landmark_dataset/landmarks.npy')
labels = np.load('landmark_dataset/labels.npy')

# Reshape landmarks to add a channel (batch size, length, channels)
landmarks = landmarks.reshape(landmarks.shape[0], landmarks.shape[1], landmarks.shape[2])

# Convert labels to categorical ((i dont fully know how this works LMAO))
num_classes = len(np.unique(labels))
labels = to_categorical(labels, num_classes=num_classes)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(landmarks, labels, test_size=0.2, random_state=1111)

# Define the model
# IDK WHAT THESE PARAMETERS DO YET WILL LOOK INTO IT FURTHER

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
# Compile and train the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

# Evaluate model accuracy
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# Save the model
model.save('hand_gesture_instrument_model.keras')