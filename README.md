# Hands-On-Sound

Hands-On-Sound is a Python app that uses hand gestures to play digital instrument sounds.

It combines:
- a camera feed for hand tracking
- MediaPipe and OpenCV for landmark detection
- a trained Keras model for gesture classification
- Pygame for audio playback

Supported instruments include violin, flute, trumpet, and snare drum.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the app from the repository root so relative asset paths resolve correctly.

## Run

```powershell
python Main.py
```

Make sure your camera is connected and available before starting the app.

## Project Files

- `Main.py` - compatibility launcher for the app
- `hands_on_sound/` - runtime app, settings UI, sound playback, and shared paths
- `assets/` - instrument sounds and Keras model artifacts
- `ml/` - model training and evaluation scripts
- `data/` - landmark arrays, collected images, and dataset creation scripts
- `tools/` - image collection and sound generation utilities

## Runtime Flow

1. `Main.py` imports and starts `hands_on_sound.app.main()`.
2. The app shows a small settings window for key and mode selection.
3. The model is loaded from `assets/models/`.
4. Frames from the camera are processed with MediaPipe hand landmarks.
5. The gesture model selects an instrument, and the hand position selects the note and volume.
6. Pygame plays the matching sampled sound from `assets/sounds/`.

## Development Scripts

Run model and dataset scripts from the repository root:

```powershell
python ml\evaluate_model.py
python ml\train_model.py
python ml\check_arrays.py
python data\create_landmark_dataset.py
python tools\collect_images.py
```

## Assets

- `assets/models/` stores the active `.keras` model and archived training artifacts.
- `assets/sounds/` stores instrument samples grouped by instrument name.
- `data/landmarks/` stores the generated `.npy` arrays used for training and evaluation.
- `data/images/data/` stores collected gesture images used to build the landmark dataset.
