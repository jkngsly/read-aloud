import { useState } from 'react'
import './App.css'

function App() {
  const [url, setUrl] = useState("")
  const [audioSrc, setAudioSrc] = useState("")

  const handlePlay = () => { 
    if(!url) return
    setAudioSrc(`http://localhost:5000/read-aloud?url=${encodeURIComponent(url)}`)
  }

  return (
    <>
      <div>
        <h2>Article Read-Aloud</h2>
        <input
          type="text"
          placeholder="Enter article URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button onClick={handlePlay}>Play</button>
        {audioSrc && <audio controls autoPlay src={audioSrc} />}
      </div>
    </>
  )
}

export default App
