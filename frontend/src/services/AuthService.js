import axios from 'axios'

export const AuthService = {
  async login(username, password) {
    const response = await axios.post('/api/token/', { username, password })
    return response.data
  },

  async register(username, fullname, email, password) {
    const response = await axios.post('/api/register/', { username, fullname, email, password })
    return response.data
  },

  async fetchProfile() {
    const response = await axios.get('/api/profile/')
    return response.data
  },

  async updateProfile(profileData) {
    const response = await axios.post('/api/profile/', profileData)
    return response.data
  }
}
