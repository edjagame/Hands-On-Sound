export interface AppSettings {
  key: ScaleKey
  mode: ScaleMode
  numNotes: number
  noteReleaseMs: number
}

export const SCALE_KEYS = [
  'C',
  'D',
  'E',
  'G',
  'A',
  'B',
  'F#',
  'C#',
  'Ab',
  'Eb',
  'Bb',
  'F',
] as const

export const SCALE_MODES = ['major', 'minor'] as const
export const MIN_NOTE_RELEASE_MS = 0
export const MAX_NOTE_RELEASE_MS = 500
export const NOTE_RELEASE_STEP_MS = 25

export type ScaleKey = (typeof SCALE_KEYS)[number]
export type ScaleMode = (typeof SCALE_MODES)[number]

export const DEFAULT_SETTINGS: AppSettings = {
  key: 'C',
  mode: 'major',
  numNotes: 7,
  noteReleaseMs: 150,
}
