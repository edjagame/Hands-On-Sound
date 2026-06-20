import numpy as np
from pathlib import Path
import sys

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import random

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hands_on_sound.paths import ACTIVE_MODEL_PATH, LABELS_PATH, LANDMARKS_PATH

# Load the landmark data.
landmarks = np.load(LANDMARKS_PATH)
labels = np.load(LABELS_PATH)

# Reshape landmarks to add a channel (batch size, length, channels)
landmarks = landmarks.reshape(landmarks.shape[0], landmarks.shape[1], landmarks.shape[2])

# Convert labels to categorical ((i dont fully know how this works LMAO))
num_classes = len(np.unique(labels))
labels = to_categorical(labels, num_classes=num_classes)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(landmarks, labels, test_size=0.2, random_state=random.randint(0, 10000))

#Loads the gesture prediciton model
model = load_model(str(ACTIVE_MODEL_PATH))

# --- Precision, Recall, and Confusion Matrix Calculation ---

# Generate predictions
y_pred_probs = model.predict(X_test)

# Convert predicted probabilities to class labels
y_pred = np.argmax(y_pred_probs, axis=1)

# Convert one-hot encoded true labels back to class labels
y_true = np.argmax(y_test, axis=1)

# Calculate precision, recall, and f1 score
precision = precision_score(y_true, y_pred, average='weighted')
recall = recall_score(y_true, y_pred, average='weighted')
f1score = f1_score(y_true, y_pred, average='weighted')

print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"F1 Score: {f1score * 100:.2f}%")

# --- Confusion Matrix ---

# Compute confusion matrix
cm = confusion_matrix(y_true, y_pred)

# Display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap=plt.cm.Blues)

# Show the plot
plt.show()

# Evaluation Tests for Training Data
# Evaluate model accuracy on training data
training_loss, training_accuracy = model.evaluate(X_train, y_train)
print(f"Training Accuracy: {training_accuracy * 100:.2f}%")

# Save the model
# model.save('hand_gesture_instrument_model.keras')
# model.save('hand_gesture_instrument_model_test.keras')

# --- Precision, Recall, and Confusion Matrix Calculation on Training Data ---

# Generate predictions on training data
y_pred_probs_train = model.predict(X_train)

# Convert predicted probabilities to class labels
y_pred_train = np.argmax(y_pred_probs_train, axis=1)

# Convert one-hot encoded true labels back to class labels
y_true_train = np.argmax(y_train, axis=1)

# Calculate precision and recall on training data
precision_train = precision_score(y_true_train, y_pred_train, average='weighted')
recall_train = recall_score(y_true_train, y_pred_train, average='weighted')
f1score_train = f1_score(y_true_train, y_pred_train, average='weighted')

print(f"Training Precision: {precision_train * 100:.2f}%")
print(f"Training Recall: {recall_train * 100:.2f}%")
print(f"Training F1 Score: {f1score_train * 100:.2f}%")

# --- Confusion Matrix on Training Data ---

# Compute confusion matrix for training data
cm_train = confusion_matrix(y_true_train, y_pred_train)

# Display confusion matrix
disp_train = ConfusionMatrixDisplay(confusion_matrix=cm_train)
disp_train.plot(cmap=plt.cm.Blues)

# Show the plot
plt.show()

# # summarize history for accuracy
# plt.plot(history.history['accuracy'])
# plt.plot(history.history['val_accuracy'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['Train', 'Validation'], loc='upper left')
# plt.show()
# # summarize history for loss
# plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['Train', 'Validation'], loc='upper left')
# plt.show()
