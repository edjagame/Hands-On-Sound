import type { AudioEngine, AudioVoiceId, Instrument } from './types'

interface VoiceState {
  audio: HTMLAudioElement
  instrument: Exclude<Instrument, 'silent'>
  key: string
}

interface ReleaseState {
  audio: HTMLAudioElement
  animationFrameId: number
}

const DEFAULT_RELEASE_MS = 150
const MIN_RELEASE_MS = 0
const MAX_RELEASE_MS = 500

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
  private releases = new Set<ReleaseState>()
  private releaseMs = DEFAULT_RELEASE_MS

  setReleaseMs(releaseMs: number): void {
    if (!Number.isFinite(releaseMs)) {
      return
    }

    this.releaseMs = Math.min(
      Math.max(releaseMs, MIN_RELEASE_MS),
      MAX_RELEASE_MS,
    )
  }

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

    this.voices.set(voiceId, { audio, instrument, key })

    void audio.play().catch((error: unknown) => {
      console.error('Audio playback failed:', error)

      if (this.voices.get(voiceId)?.audio === audio) {
        this.stop(voiceId)
      }
    })
  }

  stop(voiceId: AudioVoiceId): void {
    const voice = this.voices.get(voiceId)

    if (!voice) {
      return
    }

    this.voices.delete(voiceId)

    if (voice.instrument === 'snare' || this.releaseMs <= 0) {
      this.stopVoiceImmediately(voice.audio)
      return
    }

    this.releaseVoice(voice.audio)
  }

  private releaseVoice(audio: HTMLAudioElement): void {
    const startTime = performance.now()
    const startVolume = audio.volume
    const releaseMs = this.releaseMs
    const releaseState: ReleaseState = {
      audio,
      animationFrameId: 0,
    }

    const fadeOut = (timestamp: number) => {
      const elapsedMs = Math.max(timestamp - startTime, 0)
      const progress = Math.min(elapsedMs / releaseMs, 1)
      audio.volume = startVolume * (1 - progress)

      if (progress < 1) {
        releaseState.animationFrameId = requestAnimationFrame(fadeOut)
        return
      }

      this.releases.delete(releaseState)
      this.stopVoiceImmediately(audio)
    }

    this.releases.add(releaseState)
    releaseState.animationFrameId = requestAnimationFrame(fadeOut)
  }

  private stopVoiceImmediately(audio: HTMLAudioElement): void {
    audio.pause()
    audio.currentTime = 0
  }

  stopAll(): void {
    for (const voice of this.voices.values()) {
      this.stopVoiceImmediately(voice.audio)
    }

    this.voices.clear()

    for (const release of this.releases) {
      cancelAnimationFrame(release.animationFrameId)
      this.stopVoiceImmediately(release.audio)
    }

    this.releases.clear()
  }

  dispose(): void {
    this.stopAll()
  }
}
