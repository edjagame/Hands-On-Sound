import json
import numpy as np
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GESTURE_CONTRACT_PATH = REPO_ROOT / "hands-on-sound" / "src" / "gesture.ts"


def load_gesture_labels():
    """Load the browser gesture order used by ONNX inference."""
    source = GESTURE_CONTRACT_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"export\s+const\s+GESTURES\s*=\s*\[(.*?)\]\s*as\s+const",
        source,
        flags=re.DOTALL,
    )

    if not match:
        raise ValueError(f"Could not find GESTURES in {GESTURE_CONTRACT_PATH}")

    labels = re.findall(r"['\"]([^'\"]+)['\"]", match.group(1))

    if not labels:
        raise ValueError(f"GESTURES is empty in {GESTURE_CONTRACT_PATH}")

    if len(labels) != len(set(labels)):
        raise ValueError(f"GESTURES contains duplicate labels: {labels}")

    return labels


GESTURE_TO_ID = {
    gesture: index for index, gesture in enumerate(load_gesture_labels())
}


def process_annotations(file_path="annotations/train/", output_labels="labels.npy", output_landmarks="landmarks.npy"):
    """Convert annotation JSON files into aligned NumPy feature/label arrays."""
    all_labels = []
    all_landmarks = []

    # Gather valid, known gestures from every annotation file in the split.
    for file in Path(file_path).glob("*.json"):
        print(f"Processing {file.name}...")
        with open(file, "r") as f:
            data = json.load(f)
            for entry_id, entry in data.items():
                label_id = GESTURE_TO_ID.get(entry["labels"][0])
                if label_id is None:
                    print(f"  Skipping unknown label: {entry['labels'][0]}")
                    continue

                landmarks = entry["hand_landmarks"][0]
                if len(landmarks) != 21:
                    continue
                all_labels.append(label_id)
                all_landmarks.append(landmarks)

    # Preserve each hand as 21 x/y points; the PyTorch model flattens this to
    # 42 features during its forward pass.
    labels_arr = np.array(all_labels, dtype=np.int32)
    landmarks_arr = np.array(all_landmarks, dtype=np.float32)

    # Save matching arrays that can be loaded directly by the Dataset class.
    np.save(output_labels, labels_arr)
    np.save(output_landmarks, landmarks_arr)


def load_and_print_npy(path):
    """Print a saved array for quick preprocessing diagnostics."""
    try:
        arr = np.load(path, allow_pickle=True)
    except Exception as e:
        print(f"Failed to load '{path}': {e}")
        return
    print(f"\nContents of {path} — shape {arr.shape}:")
    print(arr)


if __name__ == "__main__":
    # Generate independent arrays for evaluation, training, and validation.
    process_annotations("annotations/test/", "labels_test.npy", "landmarks_test.npy")
    process_annotations("annotations/train/", "labels_train.npy", "landmarks_train.npy")
    process_annotations("annotations/val/", "labels_val.npy", "landmarks_val.npy")
