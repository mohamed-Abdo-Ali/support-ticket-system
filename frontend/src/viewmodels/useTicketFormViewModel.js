import { ref } from 'vue'
import { TicketService } from '../services/TicketService.js'

export function useTicketFormViewModel() {
  const subject = ref('')
  const description = ref('')
  const priority = ref('Medium')
  const category = ref('General')
  const file = ref(null)

  const error = ref('')
  const loading = ref(false)

  const handleFileChange = (e) => {
    file.value = e.target.files[0]
  }

  const handleSubmit = async (translateFn, callback) => {
    error.value = ''
    if (!subject.value || subject.value.length < 5) {
      error.value = translateFn ? translateFn('Subject must be at least 5 characters.') : 'Subject must be at least 5 characters.'
      return
    }

    loading.value = true
    try {
      const formData = new FormData()
      formData.append('subject', subject.value)
      formData.append('description', description.value)
      formData.append('priority', priority.value)
      formData.append('category', category.value)
      if (file.value) {
        formData.append('attachment', file.value)
      }

      await TicketService.createTicket(formData)
      if (callback) callback()
    } catch (err) {
      if (err.response && err.response.data && err.response.data.detail) {
        error.value = err.response.data.detail
      } else if (err.response && err.response.data && err.response.data.subject) {
        error.value = err.response.data.subject[0]
      } else {
        error.value = translateFn ? translateFn('Failed to create ticket.') : 'Failed to create ticket.'
      }
    } finally {
      loading.value = false
    }
  }

  return {
    subject,
    description,
    priority,
    category,
    file,
    error,
    loading,
    handleFileChange,
    handleSubmit
  }
}
