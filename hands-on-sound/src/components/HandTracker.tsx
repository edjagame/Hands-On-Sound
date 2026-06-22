import { useEffect, useRef } from 'react'
import type { RefObject } from 'react'
import {
  FilesetResolver,
  HandLandmarker,
} from '@mediapipe/tasks-vision'
import type { HandLandmarkerResult } from '@mediapipe/tasks-vision'

interface HandTrackerProps {
  videoRef: RefObject<HTMLVideoElement | null>
  isCameraOn: boolean
  onResults: (results: HandLandmarkerResult) => void
}

function HandTracker({ videoRef, isCameraOn, onResults }: HandTrackerProps) {
  const landmarkerRef = useRef<HandLandmarker | null>(null)

  useEffect(() => {
    let cancelled: boolean = false
    let instance: HandLandmarker | null = null

    async function initializeMediaPipe() {
      const vision = await FilesetResolver.forVisionTasks(
        'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.35/wasm',
      )

      instance = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath: 'models/hand_landmarker.task',
          delegate: 'GPU'
        },
        runningMode: 'VIDEO',
        numHands: 2,
        minHandDetectionConfidence: 0.5,
        minHandPresenceConfidence: 0.5,
        minTrackingConfidence: 0.5,
      })

      if (cancelled) {
        instance.close()
        return
      }

      landmarkerRef.current = instance
    }

    void initializeMediaPipe()

    return () => {
      cancelled = true
      instance?.close()

      if (landmarkerRef.current === instance) {
        landmarkerRef.current = null
      }
    }
  }, [])

  useEffect(() => {
    if (!isCameraOn) return

    let animationFrameId: number
    let lastVideoTime = -1

    function renderLoop(timestamp: number): void {
      const video = videoRef.current
      const landmarker = landmarkerRef.current

      if (
        video &&
        landmarker &&
        video.readyState >= HTMLMediaElement.HAVE_CURRENT_DATA
      ) {
        if (video.currentTime !== lastVideoTime) {
          lastVideoTime = video.currentTime
          const detections = landmarker.detectForVideo(video, timestamp)
          onResults(detections)
        }
      }
      animationFrameId = requestAnimationFrame(renderLoop)
    }

    animationFrameId = requestAnimationFrame(renderLoop)

    return () => {
      cancelAnimationFrame(animationFrameId)
    }
  }, [isCameraOn, videoRef, onResults])

  return null
}

export default HandTracker
