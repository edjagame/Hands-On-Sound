import CameraPreview from './components/CameraPreview'
import { useState } from 'react'
import Settings from './components/Settings'
import { DEFAULT_SETTINGS, type AppSettings } from './settings'
import './App.css'

function App() {
  const [settings, setSettings] = useState<AppSettings>(DEFAULT_SETTINGS)

  return (
    <div className="app">
      <header className="app-header" />
      <main className="app-main">
        <section className="app-column app-column-left">
          <div className="app-intro" aria-label="Gesture guide">
            <h1>Hands on Sound</h1>
            <p>
              Play instruments with hand gestures, then move your hands through
              the camera view to change notes and volume.
            </p>
            <div className="app-guide">
              <h2>Gestures</h2>
              <ul>
                <li>Fist: violin</li>
                <li>OK: flute</li>
                <li>Rock: trumpet</li>
                <li>Peace: snare drum</li>
                <li>Palm or stop: silence</li>
              </ul>
            </div>
            <div className="app-guide">
              <h2>Volume</h2>
              <p>
                Raise your hand for louder sound. Lower your hand for softer
                sound.
              </p>
            </div>
          </div>
        </section>
        <section className="app-column app-column-center">
          <CameraPreview settings={settings} />
        </section>
        <section className="app-column app-column-right">
          <Settings
            settings={settings}
            onSettingsChange={setSettings}
          />
        </section>
      </main>
      <footer className="app-footer" />
    </div>
  )
}

export default App
