import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  withCredentials: true, // Crucial for HttpOnly cookies
  headers: {
    'Content-Type': 'application/json',
  },
})

// Optional: Add response interceptors for global error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login or clear auth state if unauthorized
      console.warn('Unauthorized access - potential session expiration')
    }
    return Promise.reject(error)
  }
)

export default apiClient
