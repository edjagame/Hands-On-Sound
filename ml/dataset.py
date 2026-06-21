import numpy as np
import torch
from torch.utils.data import Dataset


class HandLandmarkDataset(Dataset):
    def __init__(self, landmarks_path, labels_path):
        # Load the preprocessed MediaPipe coordinates and integer class labels.
        landmarks = np.load(landmarks_path).astype(np.float32)
        labels = np.load(labels_path).astype(np.int64)

        # Every sample should contain 21 hand landmarks with x/y coordinates.
        if landmarks.ndim != 3 or landmarks.shape[1:] != (21, 2):
            raise ValueError(
                f"Expected landmarks with shape (samples, 21, 2), got {landmarks.shape}"
            )
        if len(landmarks) != len(labels):
            raise ValueError(
                f"Landmark and label counts differ: {len(landmarks)} != {len(labels)}"
            )

        # Keep the geometric 21x2 layout here; the classifier flattens each
        # sample to 42 features immediately before its first linear layer.
        self.x = torch.from_numpy(landmarks)
        self.y = torch.from_numpy(labels)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]
