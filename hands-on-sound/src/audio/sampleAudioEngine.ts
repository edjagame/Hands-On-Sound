import type { AudioEngine, Instrument } from './types'

function getSampleUrl(instrument: Exclude<Instrument, 'silent'>, note: string) {
  const fileName = `${encodeURIComponent(note)}.wav`

  return `${import.meta.env.BASE_URL}sounds/${instrument}/${fileName}`
}

export class SampleAudioEngine implements AudioEngine {
  private currentAudio: HTMLAudioElement | null = null
  private currentKey: string | null = null

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
