import { useEffect, useRef, useState } from 'react'
import HandTracker from './HandTracker'
import HandCanvas from './HandCanvas'
import type { HandLandmarkerResult } from '@mediapipe/tasks-vision'

const CAMERA_SIZE = {
  width:640,
  height:360
}

function stopMediaStream(stream: MediaStream | null) {
  stream?.getTracks().forEach((track) => track.stop())
}

function CameraPreview() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const [isCameraOn, setIsCameraOn] = useState(false)
  const [isCameraStarting, setIsCameraStarting] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [results, setResults] = useState<HandLandmarkerResult | null>(null)

  async function startCamera() {
    setErrorMessage(null)
    setIsCameraStarting(true)

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'user',
          width: { ideal: CAMERA_SIZE.width },
          height: { ideal: CAMERA_SIZE.height },
        },
        audio: false,
      })

      // Keep the stream outside React state because it is a mutable browser resource.
      streamRef.current = stream

      if (videoRef.current) {
        videoRef.current.srcObject = stream
      }

      setIsCameraOn(true)
    } catch {
      setErrorMessage(
        'Failed to access the camera. Check your browser permissions.',
      )
    } finally {
      setIsCameraStarting(false)
    }
  }

  function stopCamera() {
    stopMediaStream(streamRef.current)
    streamRef.current = null

    if (videoRef.current) {
      videoRef.current.srcObject = null
    }

    setResults(null)
    setIsCameraOn(false)
  }

  function toggleCamera() {
    if (isCameraOn) {
      stopCamera()
      return
    }

    void startCamera()
  }

  useEffect(() => {
    // Release the camera if the component is removed while the stream is active.
    return () => stopMediaStream(streamRef.current)
  }, [])

  return (
    <div className="camera">
      <div className="camera-display">
        <video ref={videoRef} autoPlay muted playsInline />
        <HandCanvas 
          results={results} 
          canvasWidth={CAMERA_SIZE.width}
          canvasHeight={CAMERA_SIZE.height}
        />
      </div>
      <HandTracker
        videoRef={videoRef}
        isCameraOn={isCameraOn}
        onResults={setResults}
      />

      <button
        type="button"
        onClick={toggleCamera}
        disabled={isCameraStarting}
      >
        {isCameraStarting
          ? 'Starting Camera...'
          : isCameraOn
            ? 'Stop Camera'
            : 'Start Camera'}
      </button>

      {errorMessage && <p role="alert">{errorMessage}</p>}
    </div>
  )
}

export default CameraPreview
