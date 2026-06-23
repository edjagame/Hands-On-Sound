import type { NormalizedLandmark } from '@mediapipe/tasks-vision'
import * as ort from 'onnxruntime-web'
import { GESTURES, type GesturePrediction } from '../gesture'

const sessionPromise = ort.InferenceSession.create(
  `${import.meta.env.BASE_URL}models/hand_sign_model.onnx`,
  {
    executionProviders: ['wasm'],
  },
)

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

function softmax(logits: number[]): number[] {
  const maxLogit = Math.max(...logits)

  const exponentials = logits.map((logit) =>
    Math.exp(logit - maxLogit),
  )

  const total = exponentials.reduce(
    (sum, value) => sum + value,
    0,
  )

  return exponentials.map((value) => value / total)
}

export async function classifyGesture(
  landmarks: NormalizedLandmark[],
): Promise<GesturePrediction> {
  const session = await sessionPromise
  const inputTensor = createInputTensor(landmarks)

  const results = await session.run({
    [session.inputNames[0]]: inputTensor,
  })

  const outputTensor = results[session.outputNames[0]]
  const logits = Array.from(outputTensor.data, Number)
  const probabilities = softmax(logits)


  let predictedIndex = 0

  for (let index = 1; index < probabilities.length; index += 1) {
    if (probabilities[index] > probabilities[predictedIndex]) {
      predictedIndex = index
    }
  }

  return {
    gesture: GESTURES[predictedIndex],
    confidence: probabilities[predictedIndex],
  }
}
