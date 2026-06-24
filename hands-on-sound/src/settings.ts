export interface AppSettings {
  key: ScaleKey
  mode: ScaleMode
  numNotes: number
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

export type ScaleKey = (typeof SCALE_KEYS)[number]
export type ScaleMode = (typeof SCALE_MODES)[number]

export const DEFAULT_SETTINGS: AppSettings = {
  key: 'C',
  mode: 'major',
  numNotes: 7,
}
