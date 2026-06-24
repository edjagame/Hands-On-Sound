import type { ScaleKey, ScaleMode } from '../settings'

const MAX_PLAYABLE_NOTES = 8
const DEFAULT_NOTE = 'C4'

const MAJOR_SCALES: Record<ScaleKey, readonly string[]> = {
  C: ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
  D: ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
  E: ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
  G: ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
  A: ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
  B: ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
  'F#': ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'],
  'C#': ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'],
  Ab: ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
  Eb: ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
  Bb: ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
  F: ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
}

const MINOR_SCALES: Record<ScaleKey, readonly string[]> = {
  C: ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'],
  D: ['D', 'E', 'F', 'G', 'A', 'Bb', 'C'],
  E: ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],
  G: ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F'],
  A: ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
  B: ['B', 'C#', 'D', 'E', 'F#', 'G', 'A'],
  'F#': ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E'],
  'C#': ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B'],
  Ab: ['Ab', 'Bb', 'B', 'Db', 'Eb', 'E', 'F#'],
  Eb: ['Eb', 'F', 'Gb', 'Ab', 'Bb', 'B', 'Db'],
  Bb: ['Bb', 'C', 'Db', 'Eb', 'F', 'Gb', 'Ab'],
  F: ['F', 'G', 'Ab', 'Bb', 'C', 'Db', 'Eb'],
}

const SAMPLE_NOTE_NAMES: Record<string, string> = {
  C: 'C',
  'B#': 'C',
  'C#': 'C#',
  Db: 'C#',
  D: 'D',
  'D#': 'D#',
  Eb: 'D#',
  E: 'E',
  Fb: 'E',
  F: 'F',
  'E#': 'F',
  'F#': 'F#',
  Gb: 'F#',
  G: 'G',
  'G#': 'G#',
  Ab: 'G#',
  A: 'A',
  'A#': 'A#',
  Bb: 'A#',
  B: 'B',
  Cb: 'B',
}

const NOTE_SEMITONES: Record<string, number> = {
  C: 0,
  'B#': 0,
  'C#': 1,
  Db: 1,
  D: 2,
  'D#': 3,
  Eb: 3,
  E: 4,
  Fb: 4,
  F: 5,
  'E#': 5,
  'F#': 6,
  Gb: 6,
  G: 7,
  'G#': 8,
  Ab: 8,
  A: 9,
  'A#': 10,
  Bb: 10,
  B: 11,
  Cb: 11,
}

function getScaleNotes(key: ScaleKey, mode: ScaleMode): readonly string[] {
  return mode === 'major' ? MAJOR_SCALES[key] : MINOR_SCALES[key]
}

function clampNoteCount(noteCount: number): number {
  if (!Number.isFinite(noteCount)) {
    return 1
  }

  return Math.min(
    Math.max(1, Math.floor(noteCount)),
    MAX_PLAYABLE_NOTES,
  )
}

function getSampleNoteName(noteName: string): string {
  return SAMPLE_NOTE_NAMES[noteName] ?? noteName
}

export function getPlayableNotes(
  key: ScaleKey,
  mode: ScaleMode,
  requestedNoteCount: number,
): string[] {
  const noteCount = clampNoteCount(requestedNoteCount)
  const scaleNotes = getScaleNotes(key, mode)
  const notes: string[] = []
  let octave = 4
  let previousSemitone: number | null = null

  for (let index = 0; index < noteCount; index += 1) {
    const noteName = scaleNotes[index % scaleNotes.length]
    const semitone = NOTE_SEMITONES[noteName]

    if (
      previousSemitone !== null &&
      semitone <= previousSemitone
    ) {
      octave += 1
    }

    notes.push(`${getSampleNoteName(noteName)}${octave}`)
    previousSemitone = semitone
  }

  return notes
}

export function getAvailableNoteCount(): number {
  return MAX_PLAYABLE_NOTES
}

export function getDefaultNote(): string {
  return DEFAULT_NOTE
}

export function getNoteForHandPosition(
  normalizedX: number | undefined,
  requestedNoteCount: number,
  key: ScaleKey,
  mode: ScaleMode,
): string {
  const noteCount = clampNoteCount(requestedNoteCount)
  const availableNotes = getPlayableNotes(key, mode, noteCount)

  if (normalizedX === undefined || !Number.isFinite(normalizedX)) {
    return availableNotes[0] ?? DEFAULT_NOTE
  }

  const boundedX = Math.min(Math.max(normalizedX, 0), 1)
  const noteIndex = Math.min(
    Math.floor(boundedX * noteCount),
    noteCount - 1,
  )

  return availableNotes[noteIndex] ?? DEFAULT_NOTE
}
