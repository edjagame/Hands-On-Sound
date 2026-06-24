import { useEffect, useRef } from 'react'
import type {
  HandLandmarkerResult,
  NormalizedLandmark,
} from '@mediapipe/tasks-vision'
import { classifyGesture } from '../classification/gestureClassifier'
import type {
  Gesture,
  GesturePrediction,
  HandGesturePredictions,
  HandId,
} from '../gesture'
import { getDetectedHands } from '../hands'

interface GestureClassifierProps {
  results: HandLandmarkerResult | null
  onPredictionChange: (predictions: HandGesturePredictions) => void
}

const HISTORY_SIZE = 5

function getMajorityPrediction(
  predictions: GesturePrediction[],
): GesturePrediction {
  const counts = new Map<Gesture, number>()

  for (const prediction of predictions) {
    counts.set(
      prediction.gesture,
      (counts.get(prediction.gesture) ?? 0) + 1,
    )
  }

  return predictions.reduce((winner, prediction) => {
    const winnerCount = counts.get(winner.gesture) ?? 0
    const predictionCount = counts.get(prediction.gesture) ?? 0

    return predictionCount > winnerCount ? prediction : winner
  })
}

function normalizeLandmarksForHand(
  landmarks: NormalizedLandmark[],
  handId: HandId,
): NormalizedLandmark[] {
  if (handId !== 'left') {
    return landmarks
  }

  return landmarks.map((landmark) => ({
    ...landmark,
    x: 1 - landmark.x,
  }))
}

function GestureClassifier({
  results,
  onPredictionChange,
}: GestureClassifierProps) {
  const predictionHistoryRef = useRef<
    Record<HandId, GesturePrediction[]>
  >({
    left: [],
    right: [],
  })
  const inferenceRunningRef = useRef<boolean>(false)

  useEffect(() => {
    const detectedHands = getDetectedHands(results)

    if (!detectedHands.length) {
      predictionHistoryRef.current.left = []
      predictionHistoryRef.current.right = []
      onPredictionChange({})
      return
    }

    if (inferenceRunningRef.current) return

    let cancelled = false
    inferenceRunningRef.current = true

    async function classifyDetectedHands() {
      const nextPredictions: Array<{
        handId: HandId
        prediction: GesturePrediction
      }> = []

      for (const { handId, landmarks } of detectedHands) {
        const normalizedLandmarks = normalizeLandmarksForHand(
          landmarks,
          handId,
        )
        const prediction = await classifyGesture(normalizedLandmarks)

        nextPredictions.push({ handId, prediction })
      }

      return nextPredictions
    }

    void classifyDetectedHands()
      .then((nextPredictions) => {
        if (!cancelled) {
          const visibleHands = new Set<HandId>()
          const predictions: HandGesturePredictions = {}

          for (const { handId, prediction } of nextPredictions) {
            visibleHands.add(handId)

            const history = predictionHistoryRef.current[handId]

            history.push(prediction)

            if (history.length > HISTORY_SIZE) {
              history.shift()
            }

            predictions[handId] = getMajorityPrediction(history)
          }

          for (const handId of ['left', 'right'] as const) {
            if (!visibleHands.has(handId)) {
              predictionHistoryRef.current[handId] = []
            }
          }

          onPredictionChange(predictions)
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
  }, [onPredictionChange, results])

  return null
}

export default GestureClassifier
