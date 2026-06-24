import type { AppSettings } from '../settings'
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

  return (
    <aside className="settings" aria-label="Settings">
      <h2>Settings</h2>
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
    </aside>
  )
}

export default Settings
