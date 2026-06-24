import type { HandLandmarkerResult, NormalizedLandmark } from '@mediapipe/tasks-vision'
import { getInstrumentForGesture, type Instrument } from './audio/types'
import { getDisplayNotes, getNoteForHandPosition } from './audio/notes'
import { getVolumeForHandPosition } from './audio/volume'
import type { HandGesturePredictions, GesturePrediction, HandId } from './gesture'
import { getDetectedHands } from './hands'
import type { AppSettings } from './settings'

export const HAND_IDS = ['left', 'right'] as const
export const MIN_AUDIO_CONFIDENCE = 0.6

const HAND_CENTER_LANDMARK_INDEX = 9

export interface HandPerformanceState {
  handId: HandId
  handCenter: NormalizedLandmark | undefined
  laneIndex: number | undefined
  prediction: GesturePrediction | undefined
  hasConfidentPrediction: boolean
  instrument: Instrument
  note: string
  volume: number
}

export type HandPerformanceStates = Record<HandId, HandPerformanceState>

function clampLaneIndex(laneIndex: number, laneCount: number): number {
  return Math.min(Math.max(laneIndex, 0), laneCount - 1)
}

function getLaneIndex(
  handCenter: NormalizedLandmark | undefined,
  laneCount: number,
): number | undefined {
  if (
    !handCenter ||
    !Number.isFinite(handCenter.x) ||
    laneCount < 1
  ) {
    return undefined
  }

  return clampLaneIndex(Math.floor((1 - handCenter.x) * laneCount), laneCount)
}

export function getHandPerformanceStates({
  results,
  predictions,
  settings,
  isCameraOn,
}: {
  results: HandLandmarkerResult | null
  predictions: HandGesturePredictions
  settings: AppSettings
  isCameraOn: boolean
}): HandPerformanceStates {
  const detectedHands = new Map(
    getDetectedHands(results).map((hand) => [hand.handId, hand]),
  )
  const laneCount = getDisplayNotes(
    settings.key,
    settings.mode,
    settings.numNotes,
  ).length

  return Object.fromEntries(
    HAND_IDS.map((handId) => {
      const prediction = predictions[handId]
      const handCenter =
        detectedHands.get(handId)?.landmarks[HAND_CENTER_LANDMARK_INDEX]
      const hasConfidentPrediction =
        isCameraOn &&
        prediction !== undefined &&
        prediction.confidence >= MIN_AUDIO_CONFIDENCE
      const instrument =
        hasConfidentPrediction
          ? getInstrumentForGesture(prediction.gesture)
          : 'silent'
      const noteX = handCenter ? 1 - handCenter.x : undefined
      const laneIndex = getLaneIndex(handCenter, laneCount)
      const note = getNoteForHandPosition(
        noteX,
        settings.numNotes,
        settings.key,
        settings.mode,
      )
      const volume = getVolumeForHandPosition(handCenter?.y)

      return [
        handId,
        {
          handId,
          handCenter,
          laneIndex,
          prediction,
          hasConfidentPrediction,
          instrument,
          note,
          volume,
        },
      ]
    }),
  ) as HandPerformanceStates
}
