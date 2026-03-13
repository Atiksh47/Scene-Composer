import { useState } from 'react'
import './App.css'
import { storyboardAPI } from './api'
import Storyboard from './components/Storyboard'

function App() {
  const [story, setStory] = useState('')
  const [loading, setLoading] = useState(false)
  const [scenes, setScenes] = useState([])
  const [error, setError] = useState(null)

  const handleGenerate = async () => {
    if (!story.trim()) {
      setError('Please enter a story')
      return
    }

    setLoading(true)
    setError(null)
    setScenes([])
    
    try {
      const storyboard = await storyboardAPI.generateStoryboard(story)
      setScenes(storyboard)
    } catch (error) {
      console.error('Error generating storyboard:', error)
      const errorMessage = error.response?.data?.detail || 
                          error.message || 
                          'Failed to generate storyboard. Please try again.'
      setError(errorMessage)
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
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        <div className="storyboard-section">
          {loading ? (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <div className="loading-text">Generating your storyboard... This may take a minute.</div>
            </div>
          ) : scenes.length > 0 ? (
            <Storyboard scenes={scenes} />
          ) : (
            <p className="placeholder">
              Storyboard will appear here...
            </p>
          )}
        </div>
      </main>
    </div>
  )
}

export default App

