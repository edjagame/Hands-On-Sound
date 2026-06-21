import torch
import torch.nn as nn
from pathlib import Path
from torch.utils.data import DataLoader
from dataset import HandLandmarkDataset
from model import HandSignClassifier

# --- Config ---
EPOCHS = 50
BATCH_SIZE = 32
LR = 1e-3
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DATA_DIR = Path(__file__).resolve().parent / "data"

# --- Data ---
# Load train/validation splits and form shuffled mini-batches for training.
train_ds = HandLandmarkDataset(
    DATA_DIR / "landmarks_train.npy", DATA_DIR / "labels_train.npy"
)
val_ds = HandLandmarkDataset(
    DATA_DIR / "landmarks_val.npy", DATA_DIR / "labels_val.npy"
)

train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
val_loader   = DataLoader(val_ds,   batch_size=BATCH_SIZE)

# --- Model ---
# Build the classifier from the labels present in the training split.
num_classes = len(torch.unique(train_ds.y))
model = HandSignClassifier(num_classes).to(DEVICE)

optimizer = torch.optim.Adam(model.parameters(), lr=LR)
criterion = nn.CrossEntropyLoss()

# --- Training loop ---
# Alternate gradient-based training with a no-gradient validation pass.
for epoch in range(1, EPOCHS + 1):
    model.train()
    total_loss, correct = 0, 0

    for X, y in train_loader:
        X, y = X.to(DEVICE), y.to(DEVICE)
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * len(y)
        correct += (logits.argmax(1) == y).sum().item()

    train_acc = correct / len(train_ds)
    train_loss = total_loss / len(train_ds)

    # --- Validation ---
    model.eval()
    val_correct = 0
    with torch.no_grad():
        for X, y in val_loader:
            X, y = X.to(DEVICE), y.to(DEVICE)
            val_correct += (model(X).argmax(1) == y).sum().item()

    val_acc = val_correct / len(val_ds)
    print(f"Epoch {epoch:3d} | loss {train_loss:.4f} | train acc {train_acc:.3f} | val acc {val_acc:.3f}")

# --- Save ---
# Persist only learned parameters so the same model definition can be reused.
torch.save(model.state_dict(), DATA_DIR / "hand_sign_model.pth")
print("Model saved.")
