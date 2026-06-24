export const GESTURES = [
  'fist',
  'ok',
  'palm',
  'peace',
  'rock',
  'stop',
  'no_gesture',
] as const

export type Gesture = (typeof GESTURES)[number]

export type HandId = 'left' | 'right'

export interface GesturePrediction {
  gesture: Gesture
  confidence: number
}

export type HandGesturePredictions = Partial<Record<HandId, GesturePrediction>>
