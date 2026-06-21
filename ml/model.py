import torch.nn as nn


class HandSignClassifier(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        # Classify the 42 flattened x/y coordinates through a small MLP.
        self.net = nn.Sequential(
            nn.Linear(42, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        # DataLoader batches have shape (batch, 21, 2). Linear layers expect
        # one feature axis, so flatten each sample to (batch, 42).
        x = x.flatten(start_dim=1)
        if x.shape[1] != 42:
            raise ValueError(
                f"Expected 42 landmark features per sample, got {x.shape[1]}"
            )
        return self.net(x)

