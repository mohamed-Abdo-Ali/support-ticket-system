import { ref, computed } from 'vue'
import { TicketService } from '../services/TicketService.js'
import { authState } from '../auth.js'
import { i18nState } from '../i18n.js'

export function useTicketListViewModel() {
  const tickets = ref([])
  const count = ref(0)
  const loading = ref(true)
  const error = ref('')

  const search = ref('')
  const selectedStatus = ref('')
  const selectedPriority = ref('')
  const page = ref(1)

  const locale = computed(() => i18nState.locale)
  const user = computed(() => authState.user)

  const syncFiltersFromRoute = (query) => {
    if (query.priority) {
      const p = query.priority.toLowerCase()
      if (p === 'high') selectedPriority.value = 'High'
      else if (p === 'medium') selectedPriority.value = 'Medium'
      else if (p === 'low') selectedPriority.value = 'Low'
    } else {
      selectedPriority.value = ''
    }

    if (query.status) {
      const s = query.status.toLowerCase()
      if (s === 'open') selectedStatus.value = 'Open'
      else if (s === 'in_progress' || s === 'in progress') selectedStatus.value = 'In Progress'
      else if (s === 'resolved') selectedStatus.value = 'Resolved'
      else if (s === 'closed') selectedStatus.value = 'Closed'
    } else {
      selectedStatus.value = ''
    }
  }

  const fetchTickets = async (translateFn) => {
    loading.value = true
    try {
      const params = {
        page: page.value,
        q: search.value,
        status: selectedStatus.value,
        priority: selectedPriority.value
      }
      const data = await TicketService.getTickets(params)
      tickets.value = data.results
      count.value = data.count
      error.value = ''
    } catch (err) {
      error.value = translateFn ? translateFn('Failed to load tickets.') : 'Failed to load tickets.'
    } finally {
      loading.value = false
    }
  }

  const applyFilters = (translateFn) => {
    page.value = 1
    fetchTickets(translateFn)
  }

  const resetFilters = (translateFn) => {
    search.value = ''
    selectedStatus.value = ''
    selectedPriority.value = ''
    page.value = 1
    fetchTickets(translateFn)
  }

  const totalPages = computed(() => Math.ceil(count.value / 10))

  const formatDate = (dateStr) => {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    return date.toLocaleDateString(locale.value === 'ar' ? 'ar-EG' : 'en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  }

  return {
    tickets,
    count,
    loading,
    error,
    search,
    selectedStatus,
    selectedPriority,
    page,
    locale,
    user,
    totalPages,
    syncFiltersFromRoute,
    fetchTickets,
    applyFilters,
    resetFilters,
    formatDate
  }
}
