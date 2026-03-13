import './Storyboard.css'

function Storyboard({ scenes }) {
  if (!scenes || scenes.length === 0) {
    return null
  }

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  return (
    <div className="storyboard-container">
      {scenes.map((scene) => (
        <div key={scene.scene_number} className="scene-card">
          <div className="scene-header">
            <span className="scene-number">Scene {scene.scene_number}</span>
          </div>
          
          {scene.image_url && (
            <div className="scene-image-container">
              <img 
                src={`${API_BASE_URL}${scene.image_url}`} 
                alt={`Scene ${scene.scene_number}: ${scene.description}`}
                className="scene-image"
                loading="lazy"
              />
            </div>
          )}
          
          <div className="scene-content">
            {scene.description && (
              <div className="scene-description">
                <h3>Description</h3>
                <p>{scene.description}</p>
              </div>
            )}
            
            {scene.narration && (
              <div className="scene-narration">
                <h3>Narration</h3>
                <p>{scene.narration}</p>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

export default Storyboard

