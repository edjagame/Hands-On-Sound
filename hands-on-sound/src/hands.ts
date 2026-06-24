import type {
  HandLandmarkerResult,
  NormalizedLandmark,
} from '@mediapipe/tasks-vision'
import type { HandId } from './gesture'

export interface DetectedHand {
  handId: HandId
  landmarks: NormalizedLandmark[]
}

function getPreferredHandId(
  results: HandLandmarkerResult,
  handIndex: number,
): HandId | null {
  const categoryName = results.handedness[handIndex]?.[0]?.categoryName

  if (categoryName === 'Left') {
    return 'left'
  }

  if (categoryName === 'Right') {
    return 'right'
  }

  return null
}

function getFallbackHandId(usedHandIds: Set<HandId>): HandId {
  return usedHandIds.has('left') ? 'right' : 'left'
}

export function getDetectedHands(
  results: HandLandmarkerResult | null,
): DetectedHand[] {
  if (!results) {
    return []
  }

  const usedHandIds = new Set<HandId>()
  const detectedHands: DetectedHand[] = []

  for (
    let handIndex = 0;
    handIndex < Math.min(results.landmarks.length, 2);
    handIndex += 1
  ) {
    const preferredHandId = getPreferredHandId(results, handIndex)
    const handId =
      preferredHandId && !usedHandIds.has(preferredHandId)
        ? preferredHandId
        : getFallbackHandId(usedHandIds)

    usedHandIds.add(handId)
    detectedHands.push({
      handId,
      landmarks: results.landmarks[handIndex],
    })
  }

  return detectedHands
}
