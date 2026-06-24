# Hands-On-Sound Browser App

This is the active React, TypeScript, and Vite implementation of
Hands-On-Sound.

## MVP Features

- Start and stop the browser camera from the main screen.
- Track up to two hands with MediaPipe Tasks Vision.
- Classify gestures in the browser with `onnxruntime-web`.
- Play sampled audio for each detected hand:
  - `fist` -> violin
  - `ok` -> flute
  - `rock` -> trumpet
  - `peace` -> snare drum
  - `palm`, `stop`, `no_gesture` -> silence
- Use horizontal hand position to choose notes.
- Use vertical hand position to control volume.
- Show live prediction status for left and right hands.
- Draw hand landmarks, note lanes, and the active note lane over the camera.
- Configure key, major/minor mode, note count, and release time.

## Assets

Browser-served assets live in `public/`:

- `public/models/hand_landmarker.task` - MediaPipe hand landmark model.
- `public/models/hand_sign_model.onnx` - gesture classifier model.
- `public/sounds/violin/` - violin samples.
- `public/sounds/flute/` - flute samples.
- `public/sounds/trumpet/` - trumpet samples.
- `public/sounds/snare/snare.wav` - snare sample.

## Development

Install dependencies:

```powershell
npm.cmd install
```

Run the app:

```powershell
npm.cmd run dev
```

Build and lint:

```powershell
npm.cmd run lint
npm.cmd run build
```

## Implementation Notes

- Camera capture is handled with browser media APIs.
- Hand tracking uses `@mediapipe/tasks-vision`.
- Gesture inference uses the ONNX classifier in `public/models/`.
- Audio playback uses browser audio primitives and sampled `.wav` files.
- Browser runtime code should not import Python modules or depend on OpenCV,
  Pygame, TensorFlow, or Keras.
