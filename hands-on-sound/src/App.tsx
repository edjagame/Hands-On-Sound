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
        <section className="app-column app-column-left" />
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
