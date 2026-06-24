import type { Gesture, HandId } from '../gesture'

export type Instrument = 'violin' | 'flute' | 'trumpet' | 'snare' | 'silent'
export type AudioVoiceId = HandId

export interface AudioEngine {
  play: (
    voiceId: AudioVoiceId,
    instrument: Instrument,
    note: string,
    volume: number,
  ) => void
  stop: (voiceId: AudioVoiceId) => void
  stopAll: () => void
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
