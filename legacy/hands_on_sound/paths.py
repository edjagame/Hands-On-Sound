from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

ASSETS_DIR = REPO_ROOT / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"
MODELS_DIR = ASSETS_DIR / "models"
MODEL_ARCHIVE_DIR = MODELS_DIR / "archive"
ACTIVE_MODEL_PATH = MODELS_DIR / "hand_gesture_instrument_model.pt"

DATA_DIR = REPO_ROOT / "data"
ANNOTATIONS_DIR = DATA_DIR / "annotations"
TRAINING_DATA_DIR = ANNOTATIONS_DIR / "test"
TEST_DATA_DIR = ANNOTATIONS_DIR / "test"
VALIDATION_DATA_DIR = ANNOTATIONS_DIR / "validation"
LANDMARKS_DIR = DATA_DIR / "landmarks"
LANDMARKS_PATH = LANDMARKS_DIR / "landmarks.npy"
LABELS_PATH = LANDMARKS_DIR / "labels.npy"
IMAGE_DATA_DIR = DATA_DIR / "images" / "data"
TRAINING_DATA_DIR = DATA_DIR / "training_data"

LOGS_DIR = REPO_ROOT / "logs"
