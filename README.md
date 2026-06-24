# Hands-On-Sound

Hands-On-Sound is a browser-based, gesture-controlled instrument. It uses the
camera to track hands, classifies hand gestures in the browser, and plays
sampled instruments based on the detected gesture and hand position.

The active MVP is in `hands-on-sound/`.

## MVP Features

- Browser camera capture with a start/stop control.
- MediaPipe hand landmark tracking for up to two hands.
- ONNX gesture classification in the browser.
- Gesture-to-instrument mapping:
  - `fist` plays violin.
  - `ok` plays flute.
  - `rock` plays trumpet.
  - `peace` plays snare drum.
  - `palm`, `stop`, and `no_gesture` silence the hand.
- Two-hand playback, with each detected hand controlling its own voice.
- Horizontal hand position selects notes from the active scale.
- Vertical hand position controls volume.
- Camera overlay with hand landmarks, note lanes, and the active note lane.
- Settings for key, major/minor mode, number of playable notes, and note
  release time.
- Browser-served model and sound assets under `hands-on-sound/public/`.

## Runtime Flow

```text
browser camera -> MediaPipe landmarks -> ONNX gesture classifier -> React UI -> sampled audio
```

1. The user starts the camera in the browser.
2. MediaPipe Tasks Vision detects up to two hands and returns 21 landmarks per
   hand.
3. The gesture classifier runs against each detected hand using the 21 `(x, y)`
   landmark pairs.
4. The React UI displays the camera feed, hand overlay, gesture prediction, note,
   instrument, confidence, and volume.
5. The audio engine plays the mapped sampled instrument for each hand.

## Repository Areas

- `hands-on-sound/` - active React, TypeScript, and Vite browser application.
- `hands-on-sound/public/models/` - browser-served MediaPipe and ONNX model
  artifacts.
- `hands-on-sound/public/sounds/` - sampled audio for violin, flute, trumpet,
  and snare drum.
- `ml/` - PyTorch gesture-classifier training and evaluation.
- `legacy/` - read-only behavioral reference from the previous Python desktop
  application.

## Setup

Install browser app dependencies:

```powershell
cd hands-on-sound
npm.cmd install
```

Optional Python setup for classifier work:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run The Browser App

```powershell
cd hands-on-sound
npm.cmd run dev
```

Open the local Vite URL in a browser and allow camera access when prompted.

## Verification

Browser application:

```powershell
cd hands-on-sound
npm.cmd run lint
npm.cmd run build
```

PyTorch classifier:

```powershell
.\.venv\Scripts\python.exe ml\test.py
```

## Notes

- Browser runtime code should stay independent of Python.
- Runtime code should not depend on OpenCV, Pygame, TensorFlow, or Keras.
- Static files needed by the browser should live in `hands-on-sound/public/`.
