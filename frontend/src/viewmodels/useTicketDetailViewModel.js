import { ref, computed } from 'vue'
import { TicketService } from '../services/TicketService.js'
import { ReplyService } from '../services/ReplyService.js'
import { authState } from '../auth.js'
import { i18nState } from '../i18n.js'

export function useTicketDetailViewModel() {
  const ticket = ref(null)
  const replies = ref([])
  const repliesCount = ref(0)
  const repliesPage = ref(1)
  const repliesHasNext = ref(false)
  const repliesHasPrev = ref(false)

  const replyText = ref('')
  const newStatus = ref('')

  const loading = ref(true)
  const repliesLoading = ref(false)
  const actionLoading = ref(false)
  const error = ref('')
  const message = ref('')

  const locale = computed(() => i18nState.locale)
  const user = computed(() => authState.user)

  const isSupportStaff = computed(() => user.value && user.value.is_staff && !user.value.is_superuser)
  const isAnyStaff = computed(() => user.value && user.value.is_staff)

  const fetchTicketDetails = async (ticketId, translateFn) => {
    loading.value = true
    try {
      const data = await TicketService.getTicket(ticketId)
      ticket.value = data
      newStatus.value = data.status
      await fetchReplies(ticketId)
      error.value = ''
    } catch (err) {
      error.value = translateFn ? translateFn('Failed to load ticket details.') : 'Failed to load ticket details.'
    } finally {
      loading.value = false
    }
  }

  const fetchReplies = async (ticketId) => {
    repliesLoading.value = true
    try {
      const data = await ReplyService.getReplies(ticketId, repliesPage.value)
      replies.value = data.results
      repliesCount.value = data.count
      repliesHasNext.value = data.has_next
      repliesHasPrev.value = data.has_previous
    } catch (err) {
      console.error('Failed to load replies', err)
    } finally {
      repliesLoading.value = false
    }
  }

  const handleAddReply = async (ticketId, translateFn) => {
    if (!replyText.value.trim()) return
    actionLoading.value = true
    error.value = ''
    message.value = ''
    try {
      await ReplyService.createReply(ticketId, replyText.value)
      replyText.value = ''
      repliesPage.value = 1
      await fetchReplies(ticketId)
      message.value = translateFn ? translateFn('Reply added successfully.') : 'Reply added successfully.'
    } catch (err) {
      error.value = err.response?.data?.detail || (translateFn ? translateFn('Failed to add reply.') : 'Failed to add reply.')
    } finally {
      actionLoading.value = false
    }
  }

  const handleUpdateStatus = async (ticketId, translateFn) => {
    actionLoading.value = true
    error.value = ''
    message.value = ''
    try {
      const data = await TicketService.updateTicketStatus(ticketId, newStatus.value)
      ticket.value = data
      message.value = translateFn ? translateFn('Ticket status updated.') : 'Ticket status updated.'
    } catch (err) {
      error.value = err.response?.data?.detail || (translateFn ? translateFn('Failed to update status.') : 'Failed to update status.')
    } finally {
      actionLoading.value = false
    }
  }

  const handleDeleteTicket = async (ticketId, translateFn, callback) => {
    const confirmMsg = translateFn ? translateFn('Archive this ticket?') : 'Archive this ticket?'
    if (!confirm(confirmMsg)) return
    actionLoading.value = true
    error.value = ''
    try {
      await TicketService.deleteTicket(ticketId)
      if (callback) callback()
    } catch (err) {
      error.value = err.response?.data?.detail || (translateFn ? translateFn('Failed to delete ticket.') : 'Failed to delete ticket.')
      actionLoading.value = false
    }
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    return date.toLocaleString(locale.value === 'ar' ? 'ar-EG' : 'en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return {
    ticket,
    replies,
    repliesCount,
    repliesPage,
    repliesHasNext,
    repliesHasPrev,
    replyText,
    newStatus,
    loading,
    repliesLoading,
    actionLoading,
    error,
    message,
    locale,
    user,
    isSupportStaff,
    isAnyStaff,
    fetchTicketDetails,
    fetchReplies,
    handleAddReply,
    handleUpdateStatus,
    handleDeleteTicket,
    formatDate
  }
}
