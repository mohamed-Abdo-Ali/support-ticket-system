<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { t } from '../i18n.js'
import { useTicketListViewModel } from '../viewmodels/useTicketListViewModel.js'

const route = useRoute()

const {
  tickets,
  loading,
  error,
  search,
  selectedStatus,
  selectedPriority,
  page,
  user,
  totalPages,
  syncFiltersFromRoute,
  fetchTickets,
  applyFilters,
  resetFilters,
  formatDate
} = useTicketListViewModel()

onMounted(() => {
  syncFiltersFromRoute(route.query)
  fetchTickets(t)
})

watch(page, () => {
  fetchTickets(t)
})

watch(
  () => [route.query.priority, route.query.status], 
  () => {
    syncFiltersFromRoute(route.query)
    fetchTickets(t)
  }
)
</script>

<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem;">
      <div>
        <h2 style="font-weight: 700; margin-bottom: 0.25rem;">
          {{ $t('Ticket Repository') }}
        </h2>
        <p class="text-muted" style="margin-bottom: 0;">
          {{ $t('Browse and manage all support interactions') }}
        </p>
      </div>
      <router-link to="/tickets/new" class="btn btn-primary" v-if="user && !user.is_staff">
        <span>➕</span>
        <span>{{ $t('New Ticket') }}</span>
      </router-link>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <div class="card-body">
        <form @submit.prevent="applyFilters" class="filters-grid">
          <div class="form-group" style="margin-bottom: 0;">
            <label class="form-label">{{ $t('Quick Search') }}</label>
            <input type="text" v-model="search" class="form-control" :placeholder="$t('Subject or Keyword...')" />
          </div>

          <div class="form-group" style="margin-bottom: 0;">
            <label class="form-label">{{ $t('Status') }}</label>
            <select v-model="selectedStatus" class="form-select">
              <option value="">{{ $t('All Statuses') }}</option>
              <option value="Open">{{ $t('Open') }}</option>
              <option value="In Progress">{{ $t('In Progress') }}</option>
              <option value="Resolved">{{ $t('Resolved') }}</option>
              <option value="Closed">{{ $t('Closed') }}</option>
            </select>
          </div>

          <div class="form-group" style="margin-bottom: 0;">
            <label class="form-label">{{ $t('Priority') }}</label>
            <select v-model="selectedPriority" class="form-select">
              <option value="">{{ $t('All Priorities') }}</option>
              <option value="Low">{{ $t('Low') }}</option>
              <option value="Medium">{{ $t('Medium') }}</option>
              <option value="High">{{ $t('High') }}</option>
            </select>
          </div>

          <div style="display: flex; gap: 0.5rem; justify-content: flex-end;">
            <button type="submit" class="btn btn-primary" style="flex: 1;">
              {{ $t('Filter') }}
            </button>
            <button type="button" @click="resetFilters" class="btn btn-outline" style="flex: 1;">
              {{ $t('Reset') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div class="card" v-if="!loading && tickets.length > 0">
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>{{ $t('Ticket') }}</th>
              <th>{{ $t('Priority') }}</th>
              <th>{{ $t('Status') }}</th>
              <th>{{ $t('Category') }}</th>
              <th>{{ $t('Owner') }}</th>
              <th style="text-align: end;">{{ $t('Created At') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ticket in tickets" :key="ticket.id" @click="$router.push(`/tickets/${ticket.id}`)">
              <td>
                <div style="font-weight: 600; color: var(--text-main);">{{ ticket.subject }}</div>
                <div class="text-muted" style="font-size: 0.8rem;">#{{ ticket.id }}</div>
                <span v-if="ticket.is_late" class="badge badge-late" style="margin-top: 0.25rem;">
                  {{ $t('Overdue') }}
                </span>
              </td>
              <td>
                <span :class="['badge', `badge-${ticket.priority.toLowerCase()}`]">
                  {{ $t(ticket.priority) }}
                </span>
              </td>
              <td>
                <span :class="['badge', `badge-${ticket.status === 'In Progress' ? 'progress' : ticket.status.toLowerCase()}`]">
                  {{ $t(ticket.status) }}
                </span>
              </td>
              <td>
                <span class="text-muted" style="font-size: 0.9rem;">
                  {{ $t(ticket.category) }}
                </span>
              </td>
              <td>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <div style="width: 24px; height: 24px; border-radius: 50%; background: #e2e8f0; font-size: 0.75rem; font-weight: bold; display: flex; align-items: center; justify-content: center; color: #475569;">
                    {{ ticket.created_by_name.charAt(0).toUpperCase() }}
                  </div>
                  <span style="font-size: 0.9rem;">{{ ticket.created_by_name }}</span>
                </div>
              </td>
              <td style="text-align: end; font-size: 0.85rem; color: var(--text-muted);">
                {{ formatDate(ticket.created_at) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card" v-else-if="!loading && tickets.length === 0" style="text-align: center; padding: 4rem 2rem;">
      <span style="font-size: 3rem; display: block; margin-bottom: 1rem;">📂</span>
      <h4 style="margin-bottom: 0.5rem;">{{ $t('No tickets found') }}</h4>
      <p class="text-muted">{{ $t('No tickets match your selection.') }}</p>
    </div>

    <div v-else-if="loading" style="text-align: center; padding: 4rem 2rem;">
      <p>{{ $t('Loading tickets...') }}</p>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page === 1" @click="page--" class="page-btn">
        {{ $t('Prev') }}
      </button>
      <span class="page-info">
        {{ $t('Page') }} {{ page }} / {{ totalPages }}
      </span>
      <button :disabled="page === totalPages" @click="page++" class="page-btn">
        {{ $t('Next') }}
      </button>
    </div>
  </div>
</template>
