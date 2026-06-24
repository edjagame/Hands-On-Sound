import { useCallback, useEffect, useRef, useState } from 'react'
import HandTracker from './HandTracker'
import HandCanvas from './HandCanvas'
import GestureClassifier from './GestureClassifier'
import type { HandLandmarkerResult } from '@mediapipe/tasks-vision'
import type { HandGesturePredictions, HandId } from '../gesture'
import { getDetectedHands } from '../hands'
import { SampleAudioEngine } from '../audio/sampleAudioEngine'
import { getNoteForHandPosition } from '../audio/notes'
import { getVolumeForHandPosition } from '../audio/volume'
import {
  getInstrumentForGesture,
  type Instrument,
} from '../audio/types'
import type { AppSettings } from '../settings'

const CAMERA_SIZE = {
  width:640,
  height:360
}

const MIN_AUDIO_CONFIDENCE = 0.6
const HAND_IDS = ['left', 'right'] as const

function stopMediaStream(stream: MediaStream | null) {
  stream?.getTracks().forEach((track) => track.stop())
}

function getLandmarkForHand(
  results: HandLandmarkerResult | null,
  handId: HandId,
  landmarkIndex: number,
) {
  const detectedHand = getDetectedHands(results).find(
    (hand) => hand.handId === handId,
  )

  return detectedHand?.landmarks[landmarkIndex]
}

interface CameraPreviewProps {
  settings: AppSettings
}

function CameraPreview({ settings }: CameraPreviewProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const [audioEngine] = useState(() => new SampleAudioEngine())
  const [isCameraOn, setIsCameraOn] = useState(false)
  const [isCameraStarting, setIsCameraStarting] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [results, setResults] = useState<HandLandmarkerResult | null>(null)
  const [predictions, setPredictions] = useState<HandGesturePredictions>({})

  const getHandState = useCallback((handId: HandId) => {
    const prediction = predictions[handId]
    const handCenter = getLandmarkForHand(results, handId, 9)
    const instrument: Instrument =
      isCameraOn &&
      prediction &&
      prediction.confidence >= MIN_AUDIO_CONFIDENCE
        ? getInstrumentForGesture(prediction.gesture)
        : 'silent'
    const noteX = handCenter ? 1 - handCenter.x : undefined
    const note = getNoteForHandPosition(
      noteX,
      settings.numNotes,
      settings.key,
      settings.mode,
    )
    const volume = getVolumeForHandPosition(handCenter?.y)

    return {
      prediction,
      instrument,
      note,
      volume,
    }
  }, [
    isCameraOn,
    predictions,
    results,
    settings.key,
    settings.mode,
    settings.numNotes,
  ])

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
    setPredictions({})
    audioEngine.stopAll()
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
    audioEngine.setReleaseMs(settings.noteReleaseMs)
  }, [audioEngine, settings.noteReleaseMs])

  useEffect(() => {
    // Release the camera if the component is removed while the stream is active.
    return () => {
      stopMediaStream(streamRef.current)
      audioEngine.dispose()
    }
  }, [audioEngine])

  useEffect(() => {
    for (const handId of HAND_IDS) {
      const { instrument, note, volume } = getHandState(handId)

      if (instrument === 'silent') {
        audioEngine.stop(handId)
        continue
      }

      audioEngine.play(handId, instrument, note, volume)
    }
  }, [audioEngine, getHandState])

  function renderHandStatus(handId: HandId) {
    const { prediction, instrument, note, volume } = getHandState(handId)
    const label = handId === 'left' ? 'Left Hand' : 'Right Hand'

    if (!prediction) {
      return (
        <div className="prediction-hand" key={handId}>
          <p>{label}: no hand detected</p>
          <p>Instrument: silent</p>
          <p>Note: none</p>
          <p>Volume: none</p>
        </div>
      )
    }

    return (
      <div className="prediction-hand" key={handId}>
        <p>{label}: {prediction.gesture}</p>
        <p>Confidence: {(prediction.confidence * 100).toFixed(1)}%</p>
        <p>Instrument: {instrument}</p>
        <p>Note: {instrument === 'silent' ? 'none' : note}</p>
        <p>
          Volume:{' '}
          {instrument === 'silent'
            ? 'none'
            : `${(volume * 100).toFixed(0)}%`}
        </p>
      </div>
    )
  }

  return (
    <div className="camera">
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
      <div className="camera-display">
        <video ref={videoRef} autoPlay muted playsInline />
        <HandCanvas 
          results={results} 
          settings={settings}
          isCameraOn={isCameraOn}
          canvasWidth={CAMERA_SIZE.width}
          canvasHeight={CAMERA_SIZE.height}
        />
      </div>
      <HandTracker
        videoRef={videoRef}
        isCameraOn={isCameraOn}
        onResults={setResults}
      />
      <GestureClassifier 
        results={results}
        onPredictionChange={setPredictions}
      />
      <div className="prediction">
        {HAND_IDS.map(renderHandStatus)}
      </div>

      {errorMessage && <p role="alert">{errorMessage}</p>}
    </div>
  )
}

export default CameraPreview
