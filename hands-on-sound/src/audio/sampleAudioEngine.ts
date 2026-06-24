import type { AudioEngine, AudioVoiceId, Instrument } from './types'

interface VoiceState {
  audio: HTMLAudioElement
  key: string
}

function getSampleUrl(instrument: Exclude<Instrument, 'silent'>, note: string) {
  const fileName = `${encodeURIComponent(note)}.wav`

  return `${import.meta.env.BASE_URL}sounds/${instrument}/${fileName}`
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

    const key = `${instrument}:${note}`
    const nextVolume = Number.isFinite(volume)
      ? Math.min(Math.max(volume, 0), 1)
      : 0.75

    const currentVoice = this.voices.get(voiceId)

    if (currentVoice?.key === key) {
      currentVoice.audio.volume = nextVolume
      return
    }

    this.stop(voiceId)

    const audio = new Audio(getSampleUrl(instrument, note))
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
