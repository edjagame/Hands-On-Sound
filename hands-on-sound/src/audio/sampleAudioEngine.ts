import type { AudioEngine, Instrument } from './types'

function getSampleUrl(instrument: Exclude<Instrument, 'silent'>, note: string) {
  const fileName = `${encodeURIComponent(note)}.wav`

  return `${import.meta.env.BASE_URL}sounds/${instrument}/${fileName}`
}

export class SampleAudioEngine implements AudioEngine {
  private currentAudio: HTMLAudioElement | null = null
  private currentKey: string | null = null

  play(instrument: Instrument, note: string, volume: number): void {
    if (instrument === 'silent') {
      this.stop()
      return
    }

    const key = `${instrument}:${note}`
    const nextVolume = Number.isFinite(volume)
      ? Math.min(Math.max(volume, 0), 1)
      : 0.75

    if (this.currentKey === key && this.currentAudio) {
      this.currentAudio.volume = nextVolume
      return
    }

    this.stop()

    const audio = new Audio(getSampleUrl(instrument, note))
    audio.loop = instrument !== 'snare'
    audio.volume = nextVolume

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
}
