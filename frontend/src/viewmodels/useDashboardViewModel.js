import { ref, computed } from 'vue'
import { TicketService } from '../services/TicketService.js'
import { authState } from '../auth.js'

export function useDashboardViewModel() {
  const stats = ref({
    total_tickets: 0,
    closed_tickets: 0,
    in_progress_tickets: 0,
    open_tickets: 0,
    resolved_tickets: 0,
    high_priority_tickets: 0,
    Medium_priority_tickets: 0,
    Low_priority_tickets: 0,
    category_labels: [],
    category_counts: [],
    status_labels: [],
    status_counts: []
  })
  const loading = ref(true)
  const error = ref('')

  const user = computed(() => authState.user)

  const fetchStats = async (translateFn) => {
    loading.value = true
    try {
      const data = await TicketService.getDashboardStats()
      stats.value = data
      error.value = ''
    } catch (err) {
      error.value = translateFn ? translateFn('Failed to load dashboard data.') : 'Failed to load dashboard data.'
    } finally {
      loading.value = false
    }
  }

  return {
    stats,
    loading,
    error,
    user,
    fetchStats
  }
}
