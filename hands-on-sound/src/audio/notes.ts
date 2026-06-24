export const AVAILABLE_NOTES = [
  'C4',
  'D4',
  'E4',
  'F4',
  'G4',
  'A4',
  'B4',
  'C5',
] as const

const DEFAULT_NOTE = AVAILABLE_NOTES[0]

function clampNoteCount(noteCount: number): number {
  if (!Number.isFinite(noteCount)) {
    return 1
  }

  return Math.min(
    Math.max(1, Math.floor(noteCount)),
    AVAILABLE_NOTES.length,
  )
}

export function getAvailableNoteCount(): number {
  return AVAILABLE_NOTES.length
}

export function getDefaultNote(): string {
  return DEFAULT_NOTE
}

export function getNoteForHandPosition(
  normalizedX: number | undefined,
  requestedNoteCount: number,
): string {
  const noteCount = clampNoteCount(requestedNoteCount)

  if (normalizedX === undefined || !Number.isFinite(normalizedX)) {
    return DEFAULT_NOTE
  }

  const boundedX = Math.min(Math.max(normalizedX, 0), 1)
  const noteIndex = Math.min(
    Math.floor(boundedX * noteCount),
    noteCount - 1,
  )

  return AVAILABLE_NOTES[noteIndex]
}
