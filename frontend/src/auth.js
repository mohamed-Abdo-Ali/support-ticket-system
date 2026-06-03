import { reactive } from 'vue'
import axios from 'axios'

const API_URL = 'https://mohammed1ali.pythonanywhere.com'
axios.defaults.baseURL = API_URL

export const authState = reactive({
  isAuthenticated: !!localStorage.getItem('access_token'),
  user: JSON.parse(localStorage.getItem('user') || 'null'),
})

export const auth = {
  async login(username, password) {
    const response = await axios.post('/api/token/', { username, password })
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
    
    const profileResponse = await axios.get('/api/profile/')
    const user = profileResponse.data
    localStorage.setItem('user', JSON.stringify(user))
    
    authState.isAuthenticated = true
    authState.user = user
    return user
  },

  async register(username, fullname, email, password) {
    return axios.post('/api/register/', { username, fullname, email, password })
  },

  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    authState.isAuthenticated = false
    authState.user = null
    delete axios.defaults.headers.common['Authorization']
  },

  async fetchProfile() {
    try {
      const response = await axios.get('/api/profile/')
      localStorage.setItem('user', JSON.stringify(response.data))
      authState.user = response.data
      return response.data
    } catch (error) {
      this.logout()
      throw error
    }
  }
}

// Axios Request Interceptor
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Axios Response Interceptor for Token Expiration
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post('/api/token/refresh/', { refresh: refreshToken })
          localStorage.setItem('access_token', response.data.access)
          axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
          originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`
          return axios(originalRequest)
        } catch (refreshError) {
          auth.logout()
          window.location.href = '/login'
          return Promise.reject(refreshError)
        }
      } else {
        auth.logout()
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)
