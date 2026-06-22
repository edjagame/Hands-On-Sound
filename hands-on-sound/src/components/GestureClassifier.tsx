import { useEffect, useRef, useState } from 'react'
import type { HandLandmarkerResult } from '@mediapipe/tasks-vision'
import type { NormalizedLandmark } from '@mediapipe/tasks-vision'
import * as ort from 'onnxruntime-web';

interface GestureClassifierProps {
  results: HandLandmarkerResult | null
}

export const GESTURES = [
  'fist',
  'ok',
  'palm',
  'peace',
  'rock',
  'stop',
  'no_gesture',
] as const

const sessionPromise = ort.InferenceSession.create(
  `${import.meta.env.BASE_URL}models/hand_sign_model.onnx`,
  {
    executionProviders: ['wasm'],
  },
)

export type Gesture = (typeof GESTURES)[number]

export interface GesturePrediction {
  gesture: Gesture
  confidence: number
}

function createInputTensor(landmarks: NormalizedLandmark[]): ort.Tensor {
  if (landmarks.length !== 21) {
    throw new Error(`Expected 21 landmarks, received ${landmarks.length}`)
  }

  const values = new Float32Array(21 * 2)

  landmarks.forEach((landmark, index) => {
    values[index * 2] = landmark.x
    values[index * 2 + 1] = landmark.y
  })

  return new ort.Tensor('float32', values, [1, 21, 2])
}

async function classifyGesture(
  landmarks: NormalizedLandmark[],
): Promise<GesturePrediction> {
  const session = await sessionPromise
  const inputTensor = createInputTensor(landmarks)

  const results = await session.run({
    [session.inputNames[0]]: inputTensor,
  })

  const outputTensor = results[session.outputNames[0]]
  const logits = Array.from(outputTensor.data, Number)

  let predictedIndex = 0

  for (let index = 1; index < logits.length; index += 1) {
    if (logits[index] > logits[predictedIndex]) {
      predictedIndex = index
    }
  }

  return {
    gesture: GESTURES[predictedIndex],
    confidence: logits[predictedIndex],
  }
}

function GestureClassifier({results}: GestureClassifierProps) {
  const [prediction, setPrediction] = useState<GesturePrediction | null>(null)
  const inferenceRunningRef = useRef<boolean>(false)
  useEffect(() => {
    const landmarks = results?.landmarks[0]
    if (!landmarks) {
      setPrediction(null)
      return
    }

    if (inferenceRunningRef.current) return

    let cancelled = false
    inferenceRunningRef.current = true

    void classifyGesture(landmarks)
      .then((nextPrediction) => {
        if (!cancelled) {
          setPrediction(nextPrediction)
        }
      })
      .catch((error: unknown) => {
        console.error('Gesture classification failed:', error)
      })
      .finally(() => {
        inferenceRunningRef.current = false
      })

    return () => {
      cancelled = true
    }

  }, [results])

  if (!prediction) {
    return <p>Gesture: no hand detected</p>
  }
  return <p>Gesture: {prediction.gesture}</p>
}

export default GestureClassifier
