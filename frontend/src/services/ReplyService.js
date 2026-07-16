import axios from 'axios'

export const ReplyService = {
  async getReplies(ticketId, page = null) {
    const params = { ticket: ticketId }
    if (page) {
      params.page = page
    }
    const response = await axios.get('/api/replies/', { params })
    return response.data
  },

  async createReply(ticketId, message) {
    const response = await axios.post('/api/replies/', { ticket: ticketId, message })
    return response.data
  }
}
