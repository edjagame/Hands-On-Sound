import type { AudioEngine, AudioVoiceId, Instrument } from './types'

interface VoiceState {
  audio: HTMLAudioElement
  key: string
}

const MELODIC_SAMPLE_NOTES = new Set([
  'A#4',
  'A4',
  'B4',
  'C#4',
  'C#5',
  'C4',
  'C5',
  'D#4',
  'D#5',
  'D4',
  'D5',
  'E4',
  'E5',
  'F#4',
  'F#5',
  'F4',
  'F5',
  'G#4',
  'G#5',
  'G4',
  'G5',
])

const SHARP_TO_LOWER_NATURAL: Record<string, string> = {
  'C#': 'C',
  'D#': 'D',
  'F#': 'F',
  'G#': 'G',
  'A#': 'A',
}

function getSampleUrl(instrument: Exclude<Instrument, 'silent'>, note: string) {
  if (instrument === 'snare') {
    return `${import.meta.env.BASE_URL}sounds/snare/snare.wav`
  }

  const fileName = `${note.replace('#', '-sharp')}.wav`

  return `${import.meta.env.BASE_URL}sounds/${instrument}/${fileName}`
}

function getFallbackSampleNote(
  instrument: Exclude<Instrument, 'silent'>,
  note: string,
): string {
  if (instrument === 'snare' || MELODIC_SAMPLE_NOTES.has(note)) {
    return note
  }

  const match = note.match(/^([A-G]#?)(\d)$/)

  if (!match) {
    return note
  }

  const [, noteName, octave] = match
  const lowerNaturalNote = SHARP_TO_LOWER_NATURAL[noteName]

  if (lowerNaturalNote) {
    const naturalFallback = `${lowerNaturalNote}${octave}`

    if (MELODIC_SAMPLE_NOTES.has(naturalFallback)) {
      return naturalFallback
    }
  }

  const previousOctaveFallback = `${noteName}${Number(octave) - 1}`

  if (MELODIC_SAMPLE_NOTES.has(previousOctaveFallback)) {
    return previousOctaveFallback
  }

  return note
}

export class SampleAudioEngine implements AudioEngine {
  private voices = new Map<AudioVoiceId, VoiceState>()

  play(
    voiceId: AudioVoiceId,
    instrument: Instrument,
    note: string,
    volume: number,
  ): void {
    if (instrument === 'silent') {
      this.stop(voiceId)
      return
    }

    const sampleNote = getFallbackSampleNote(instrument, note)
    const key = instrument === 'snare' ? 'snare' : `${instrument}:${sampleNote}`
    const nextVolume = Number.isFinite(volume)
      ? Math.min(Math.max(volume, 0), 1)
      : 0.75

    const currentVoice = this.voices.get(voiceId)

    if (currentVoice?.key === key) {
      currentVoice.audio.volume = nextVolume
      return
    }

    this.stop(voiceId)

    const audio = new Audio(getSampleUrl(instrument, sampleNote))
    audio.loop = instrument !== 'snare'
    audio.volume = nextVolume

    this.voices.set(voiceId, { audio, key })

    void audio.play().catch((error: unknown) => {
      console.error('Audio playback failed:', error)
      this.stop(voiceId)
    })
  }

  stop(voiceId: AudioVoiceId): void {
    const voice = this.voices.get(voiceId)

    if (!voice) {
      return
    }

    voice.audio.pause()
    voice.audio.currentTime = 0
    this.voices.delete(voiceId)
  }

  stopAll(): void {
    for (const voiceId of this.voices.keys()) {
      this.stop(voiceId)
    }
  }

  dispose(): void {
    this.stopAll()
  }
}
