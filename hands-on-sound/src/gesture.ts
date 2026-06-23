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

export interface GesturePrediction {
  gesture: Gesture
  confidence: number
}
