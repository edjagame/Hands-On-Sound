import { useEffect, useRef, useState } from 'react'
import type { HandLandmarkerResult } from '@mediapipe/tasks-vision'
import { classifyGesture } from '../classification/gestureClassifier'
import type { GesturePrediction } from '../gesture'

interface GestureClassifierProps {
  results: HandLandmarkerResult | null
}

function GestureClassifier({results}: GestureClassifierProps) {
  const [prediction, setPrediction] = useState<GesturePrediction | null>(null)
  const inferenceRunningRef = useRef<boolean>(false)

  useEffect(() => {
    const landmarks = results?.landmarks[0]
    if (!landmarks) return

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
