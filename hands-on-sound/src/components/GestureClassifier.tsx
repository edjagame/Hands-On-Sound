import { useEffect, useRef } from 'react'
import type { HandLandmarkerResult } from '@mediapipe/tasks-vision'
import { classifyGesture } from '../classification/gestureClassifier'
import type { Gesture, GesturePrediction } from '../gesture'

interface GestureClassifierProps {
  results: HandLandmarkerResult | null
  onPredictionChange: (prediction: GesturePrediction | null) => void
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

function GestureClassifier({
  results,
  onPredictionChange,
}: GestureClassifierProps) {
  const predictionHistoryRef = useRef<GesturePrediction[]>([])
  const inferenceRunningRef = useRef<boolean>(false)

  useEffect(() => {
    const landmarks = results?.landmarks[0]
    if (!landmarks) {
      predictionHistoryRef.current = []
      onPredictionChange(null)
      return
    }

    if (inferenceRunningRef.current) return

    let cancelled = false
    inferenceRunningRef.current = true

    void classifyGesture(landmarks)
      .then((nextPrediction) => {
        if (!cancelled) {
          const history = predictionHistoryRef.current

          history.push(nextPrediction)

          if (history.length > HISTORY_SIZE) {
            history.shift()
          }

          onPredictionChange(getMajorityPrediction(history))
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
