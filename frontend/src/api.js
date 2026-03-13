import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes for storyboard generation
})

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method.toUpperCase()} request to ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      error.message = 'Request timeout. The storyboard generation is taking longer than expected. Please try with a shorter story.'
    } else if (error.code === 'ERR_NETWORK') {
      error.message = 'Network error. Please check if the backend server is running.'
    } else if (!error.response) {
      error.message = 'Unable to connect to the server. Please check your connection.'
    }
    return Promise.reject(error)
  }
)

// API functions
export const storyboardAPI = {
  /**
   * Generate a storyboard from a story
   * @param {string} story - The story text
   * @param {number|null} numScenes - Optional number of scenes
   * @returns {Promise<Array>} Array of scene objects
   */
  generateStoryboard: async (story, numScenes = null) => {
    try {
      const response = await apiClient.post('/api/generate-storyboard', {
        story,
        num_scenes: numScenes,
      })
      return response.data
    } catch (error) {
      // Error is already handled by interceptor, just rethrow
      throw error
    }
  },

  /**
   * Test Ollama connection
   * @returns {Promise<Object>} Test result
   */
  testOllama: async () => {
    try {
      const response = await apiClient.get('/api/test-ollama')
      return response.data
    } catch (error) {
      throw error
    }
  },
}

export default apiClient

