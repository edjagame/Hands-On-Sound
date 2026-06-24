import type { Gesture } from '../gesture'

export type Instrument = 'violin' | 'flute' | 'trumpet' | 'snare' | 'silent'

export interface AudioEngine {
  play: (instrument: Instrument, note: string, volume: number) => void
  stop: () => void
  dispose: () => void
}

export function getInstrumentForGesture(gesture: Gesture): Instrument {
  switch (gesture) {
    case 'fist':
      return 'violin'
    case 'ok':
      return 'flute'
    case 'rock':
      return 'trumpet'
    case 'peace':
      return 'snare'
    case 'palm':
    case 'stop':
    case 'no_gesture':
      return 'silent'
  }
}
