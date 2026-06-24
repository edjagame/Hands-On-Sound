import {
  MAX_NOTE_RELEASE_MS,
  MIN_NOTE_RELEASE_MS,
  NOTE_RELEASE_STEP_MS,
  SCALE_KEYS,
  SCALE_MODES,
  type AppSettings,
  type ScaleKey,
  type ScaleMode,
} from '../settings'
import { getAvailableNoteCount } from '../audio/notes'

interface SettingsProps {
  settings: AppSettings
  onSettingsChange: (settings: AppSettings) => void
}

function Settings({ settings, onSettingsChange }: SettingsProps) {
  function handleNumNotesChange(value: string) {
    const nextNumNotes = Number(value)

    if (!Number.isFinite(nextNumNotes)) {
      return
    }

    onSettingsChange({
      ...settings,
      numNotes: Math.max(1, nextNumNotes),
    })
  }

  function handleNoteReleaseChange(value: string) {
    const nextNoteReleaseMs = Number(value)

    if (!Number.isFinite(nextNoteReleaseMs)) {
      return
    }

    onSettingsChange({
      ...settings,
      noteReleaseMs: Math.min(
        Math.max(nextNoteReleaseMs, MIN_NOTE_RELEASE_MS),
        MAX_NOTE_RELEASE_MS,
      ),
    })
  }

  function handleKeyChange(value: string) {
    onSettingsChange({
      ...settings,
      key: value as ScaleKey,
    })
  }

  function handleModeChange(value: string) {
    onSettingsChange({
      ...settings,
      mode: value as ScaleMode,
    })
  }

  return (
    <aside className="settings" aria-label="Settings">
      <h2>Settings</h2>
      <label className="settings-field">
        <span>Key</span>
        <select
          value={settings.key}
          onChange={(event) => handleKeyChange(event.target.value)}
        >
          {SCALE_KEYS.map((key) => (
            <option key={key} value={key}>
              {key}
            </option>
          ))}
        </select>
      </label>
      <label className="settings-field">
        <span>Mode</span>
        <select
          value={settings.mode}
          onChange={(event) => handleModeChange(event.target.value)}
        >
          {SCALE_MODES.map((mode) => (
            <option key={mode} value={mode}>
              {mode === 'major' ? 'Major' : 'Minor'}
            </option>
          ))}
        </select>
      </label>
      <label className="settings-field">
        <span>Notes</span>
        <input
          type="number"
          min="1"
          max={getAvailableNoteCount()}
          value={settings.numNotes}
          onChange={(event) => handleNumNotesChange(event.target.value)}
        />
      </label>
      <label className="settings-field">
        <span>Release: {settings.noteReleaseMs} ms</span>
        <input
          type="range"
          min={MIN_NOTE_RELEASE_MS}
          max={MAX_NOTE_RELEASE_MS}
          step={NOTE_RELEASE_STEP_MS}
          value={settings.noteReleaseMs}
          onChange={(event) => handleNoteReleaseChange(event.target.value)}
        />
      </label>
    </aside>
  )
}

export default Settings
