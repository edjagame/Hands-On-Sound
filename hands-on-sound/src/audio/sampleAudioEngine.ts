import type { AudioEngine, Instrument } from './types'

const DEFAULT_NOTE = 'C4'

const FALLBACK_NOTES: Record<Exclude<Instrument, 'silent'>, string[]> = {
  violin: [DEFAULT_NOTE, 'D4', 'E4', 'F4', 'G4'],
  flute: [DEFAULT_NOTE, 'D4', 'E4', 'F4', 'G4'],
  trumpet: [DEFAULT_NOTE, 'D4', 'E4', 'F4', 'G4'],
  snare: [DEFAULT_NOTE, 'D4', 'E4', 'F4', 'G4'],
}

function getSampleUrl(instrument: Exclude<Instrument, 'silent'>, note: string) {
  const fileName = `${encodeURIComponent(note)}.wav`

  return `${import.meta.env.BASE_URL}sounds/${instrument}/${fileName}`
}

export function getDefaultNote(instrument: Instrument): string {
  if (instrument === 'silent') {
    return DEFAULT_NOTE
  }

  return FALLBACK_NOTES[instrument][0]
}

export class SampleAudioEngine implements AudioEngine {
  private currentAudio: HTMLAudioElement | null = null
  private currentKey: string | null = null
  private failedKeys = new Set<string>()

  play(instrument: Instrument, note: string): void {
    if (instrument === 'silent') {
      this.stop()
      return
    }

    const key = `${instrument}:${note}`

    if (this.currentKey === key && this.currentAudio) {
      return
    }

    this.stop()

    const audio = new Audio(getSampleUrl(instrument, note))
    audio.loop = instrument !== 'snare'
    audio.volume = 0.75

    audio.addEventListener('error', () => this.playFallback(instrument), {
      once: true,
    })

    this.currentAudio = audio
    this.currentKey = key

    void audio.play().catch((error: unknown) => {
      console.error('Audio playback failed:', error)
      this.stop()
    })
  }

  stop(): void {
    if (!this.currentAudio) {
      return
    }

    this.currentAudio.pause()
    this.currentAudio.currentTime = 0
    this.currentAudio = null
    this.currentKey = null
  }

  dispose(): void {
    this.stop()
  }

  private playFallback(instrument: Exclude<Instrument, 'silent'>): void {
    if (this.currentKey) {
      this.failedKeys.add(this.currentKey)
    }

    const fallbackNote = FALLBACK_NOTES[instrument].find((nextNote) => {
      const fallbackKey = `${instrument}:${nextNote}`

      return !this.failedKeys.has(fallbackKey)
    })

    if (fallbackNote) {
      this.play(instrument, fallbackNote)
      return
    }

    this.stop()
  }
}
