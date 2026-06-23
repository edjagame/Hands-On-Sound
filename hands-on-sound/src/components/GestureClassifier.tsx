import { useEffect, useRef, useState } from 'react'
import type { HandLandmarkerResult } from '@mediapipe/tasks-vision'
import { classifyGesture } from '../classification/gestureClassifier'
import type { Gesture, GesturePrediction } from '../gesture'

interface GestureClassifierProps {
  results: HandLandmarkerResult | null
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

function GestureClassifier({results}: GestureClassifierProps) {
  const [prediction, setPrediction] = useState<GesturePrediction | null>(null)
  const predictionHistoryRef = useRef<GesturePrediction[]>([])
  const inferenceRunningRef = useRef<boolean>(false)

  useEffect(() => {
    const landmarks = results?.landmarks[0]
    if (!landmarks) {
      predictionHistoryRef.current = []
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

          setPrediction(getMajorityPrediction(history))
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

  const hasDetectedHand = Boolean(results?.landmarks[0])

  if (!hasDetectedHand || !prediction) {
    return <p>Gesture: no hand detected</p> 
  }
  return (
    <div className = "prediction">
      <p>Gesture: {prediction.gesture}</p>
      <p>Confidence: {prediction.confidence * 100}%</p>
    </div>
  )
}

export default GestureClassifier
