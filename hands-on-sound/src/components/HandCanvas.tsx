import { useEffect, useRef } from 'react'
import { DrawingUtils, HandLandmarker } from '@mediapipe/tasks-vision'
import type { HandLandmarkerResult } from '@mediapipe/tasks-vision'
import { getDisplayNotes } from '../audio/notes'
import { HAND_IDS, type HandPerformanceStates } from '../handPerformance'
import type { AppSettings } from '../settings'

interface HandCanvasProps {
  results: HandLandmarkerResult | null
  settings: AppSettings
  isCameraOn: boolean
  handStates: HandPerformanceStates
  canvasWidth: number
  canvasHeight: number
}

function getActiveLaneIndices(
  handStates: HandPerformanceStates,
): Set<number> {
  const activeLaneIndices = new Set<number>()

  for (const handId of HAND_IDS) {
    const { laneIndex } = handStates[handId]

    if (laneIndex !== undefined) {
      activeLaneIndices.add(laneIndex)
    }
  }

  return activeLaneIndices
}

function drawNoteLanes(
  canvasCtx: CanvasRenderingContext2D,
  width: number,
  height: number,
  settings: AppSettings,
  handStates: HandPerformanceStates,
) {
  const notes = getDisplayNotes(
    settings.key,
    settings.mode,
    settings.numNotes,
  )
  const laneWidth = width / notes.length
  const activeLaneIndices = getActiveLaneIndices(handStates)

  canvasCtx.save()
  canvasCtx.textAlign = 'center'
  canvasCtx.textBaseline = 'middle'

  for (let index = 0; index < notes.length; index += 1) {
    const visualX = index * laneWidth
    const canvasX = width - visualX - laneWidth

    canvasCtx.fillStyle = 'rgba(255, 250, 240, 0.12)'
    canvasCtx.fillRect(canvasX, 0, laneWidth, height)

    if (activeLaneIndices.has(index)) {
      canvasCtx.fillStyle = 'rgba(141, 202, 105, 0.22)'
      canvasCtx.fillRect(canvasX, 0, laneWidth, height)
    }

    canvasCtx.fillStyle = 'rgba(43, 31, 18, 0.74)'
    canvasCtx.fillRect(canvasX, 0, 1, height)

    canvasCtx.strokeStyle = 'rgba(43, 31, 18, 0.78)'
    canvasCtx.lineWidth = 3
    canvasCtx.font = '700 20px Georgia, "Times New Roman", serif'

    const labelX = canvasX + laneWidth / 2
    const labelY = Math.max(24, height * 0.09)

    canvasCtx.save()
    canvasCtx.translate(labelX, labelY)
    canvasCtx.scale(-1, 1)
    canvasCtx.strokeText(notes[index], 0, 0)
    canvasCtx.restore()
  }

  canvasCtx.fillStyle = 'rgba(43, 31, 18, 0.74)'
  canvasCtx.fillRect(0, 0, 1, height)
  canvasCtx.fillRect(width - 1, 0, 1, height)

  canvasCtx.restore()
}

function drawHandCenterLandmarks(
  canvasCtx: CanvasRenderingContext2D,
  handStates: HandPerformanceStates,
  width: number,
  height: number,
) {
  canvasCtx.save()
  canvasCtx.fillStyle = '#38D45A'
  canvasCtx.strokeStyle = '#0B5F24'
  canvasCtx.lineWidth = 2

  for (const handId of HAND_IDS) {
    const { handCenter } = handStates[handId]

    if (!handCenter) {
      continue
    }

    canvasCtx.beginPath()
    canvasCtx.arc(handCenter.x * width, handCenter.y * height, 7, 0, Math.PI * 2)
    canvasCtx.fill()
    canvasCtx.stroke()
  }

  canvasCtx.restore()
}

function HandCanvas({
  results,
  settings,
  isCameraOn,
  handStates,
  canvasHeight,
  canvasWidth,
}: HandCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const canvasCtx = canvas.getContext('2d')
    if (!canvasCtx) return

    const drawingUtils = new DrawingUtils(canvasCtx)

    canvasCtx.clearRect(0, 0, canvas.width, canvas.height)

    if (isCameraOn) {
      drawNoteLanes(canvasCtx, canvas.width, canvas.height, settings, handStates)
    }

    if (!results) return

    for (const landmarks of results.landmarks) {
      drawingUtils.drawConnectors(
        landmarks,
        HandLandmarker.HAND_CONNECTIONS,
        {
          color: '#FDF8E1',
          lineWidth: 5,
        },
      )
      drawingUtils.drawLandmarks(landmarks, {
        color: '#FF6E00',
        lineWidth: 1,
      })
    }

    drawHandCenterLandmarks(canvasCtx, handStates, canvas.width, canvas.height)
  }, [results, settings, isCameraOn, handStates, canvasWidth, canvasHeight])

  return (
    <canvas
      ref={canvasRef}
      width={canvasWidth}
      height={canvasHeight}
    />
  )
}

export default HandCanvas
