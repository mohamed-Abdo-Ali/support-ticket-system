import axios from 'axios'

export const TicketService = {
  async getTickets(params) {
    const response = await axios.get('/api/tickets/', { params })
    return response.data
  },

  async getTicket(id) {
    const response = await axios.get(`/api/tickets/${id}/`)
    return response.data
  },

  async createTicket(formData) {
    // If formData is not FormData instance, convert it or send as JSON
    const headers = formData instanceof FormData ? { 'Content-Type': 'multipart/form-data' } : {}
    const response = await axios.post('/api/tickets/', formData, { headers })
    return response.data
  },

  async updateTicketStatus(id, statusValue) {
    const response = await axios.put(`/api/tickets/${id}/`, { status: statusValue })
    return response.data
  },

  async deleteTicket(id) {
    const response = await axios.delete(`/api/tickets/${id}/`)
    return response.data
  },

  async getDashboardStats() {
    const response = await axios.get('/api/dashboard/')
    return response.data
  }
}
