import axios from 'axios'

export const UserService = {
  async getUsers() {
    const response = await axios.get('/api/users/')
    return response.data
  },

  async getUser(id) {
    const response = await axios.get(`/api/users/${id}/`)
    return response.data
  },

  async createUser(userData) {
    const response = await axios.post('/api/users/', userData)
    return response.data
  },

  async updateUser(id, userData) {
    const response = await axios.put(`/api/users/${id}/`, userData)
    return response.data
  },

  async deleteUser(id) {
    const response = await axios.delete(`/api/users/${id}/`)
    return response.data
  }
}
