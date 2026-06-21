import torch
from pathlib import Path
from torch.utils.data import DataLoader
from dataset import HandLandmarkDataset
from model import HandSignClassifier

# --- Test data ---
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DATA_DIR = Path(__file__).resolve().parent / "data"
test_ds = HandLandmarkDataset(
    DATA_DIR / "landmarks_test.npy", DATA_DIR / "labels_test.npy"
)
test_loader = DataLoader(test_ds, batch_size=32)

# --- Restored model ---
num_classes = len(torch.unique(test_ds.y))
model = HandSignClassifier(num_classes).to(DEVICE)
model.load_state_dict(
    torch.load(DATA_DIR / "hand_sign_model.pth", map_location=DEVICE)
)
model.eval()

# --- Evaluation ---
# Disable gradient tracking because testing only needs forward predictions.
correct = 0
with torch.no_grad():
    for X, y in test_loader:
        X, y = X.to(DEVICE), y.to(DEVICE)
        correct += (model(X).argmax(1) == y).sum().item()

print(f"Test accuracy: {correct / len(test_ds):.3f}")
