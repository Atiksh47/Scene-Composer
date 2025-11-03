import { useState } from 'react'
import './App.css'

function App() {
  const [story, setStory] = useState('')
  const [loading, setLoading] = useState(false)

  const handleGenerate = async () => {
    // TODO: Implement storyboard generation
    setLoading(true)
    try {
      // API call will go here
      console.log('Generating storyboard for:', story)
    } catch (error) {
      console.error('Error generating storyboard:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Scene Composer</h1>
        <p>Transform your story into an illustrated storyboard</p>
      </header>
      
      <main className="app-main">
        <div className="input-section">
          <textarea
            className="story-input"
            placeholder="Enter your story idea or description here..."
            value={story}
            onChange={(e) => setStory(e.target.value)}
            rows={8}
          />
          <button 
            onClick={handleGenerate}
            disabled={!story.trim() || loading}
            className="generate-button"
          >
            {loading ? 'Generating...' : 'Generate Storyboard'}
          </button>
        </div>
        
        <div className="storyboard-section">
          {/* Storyboard will be displayed here */}
          <p className="placeholder">Storyboard will appear here...</p>
        </div>
      </main>
    </div>
  )
}

export default App

