<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { t } from '../i18n.js'
import { useUserViewModel } from '../viewmodels/useUserViewModel.js'

const route = useRoute()
const userId = route.params.id

const {
  targetUser,
  userTickets,
  loading,
  ticketsLoading,
  error,
  fetchUserDetails,
  fetchUserTickets,
  formatDate
} = useUserViewModel()

onMounted(async () => {
  await fetchUserDetails(userId, t)
  if (targetUser.value) {
    fetchUserTickets(userId)
  }
})
</script>

<template>
  <div v-if="loading" style="text-align: center; padding: 3rem;">
    <p>{{ $t('Loading user details...') }}</p>
  </div>

  <div v-else-if="error" class="alert alert-danger">
    {{ error }}
  </div>

  <div v-else-if="targetUser">
    <div style="margin-bottom: 1.5rem; display: flex; gap: 0.5rem; align-items: center; font-size: 0.9rem;">
      <router-link to="/users" style="font-weight: 500;">
        {{ $t('User Management') }}
      </router-link>
      <span class="text-muted">/</span>
      <span class="text-muted">{{ targetUser.username }}</span>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
        <span>{{ $t('User Account Info') }}</span>
        <router-link :to="`/users/${targetUser.id}/edit`" class="btn btn-primary btn-sm">
          <span>✏️</span>
          <span>{{ $t('Edit') }}</span>
        </router-link>
      </div>
      <div class="card-body">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
          <div>
            <span class="form-label">{{ $t('Username') }}</span>
            <p style="font-size: 1.1rem; font-weight: 600;">{{ targetUser.username }}</p>
          </div>
          <div>
            <span class="form-label">{{ $t('Full Name') }}</span>
            <p style="font-size: 1.1rem;">{{ targetUser.fullname || '-' }}</p>
          </div>
          <div>
            <span class="form-label">{{  $t('Email Address')  }}</span>
            <p style="font-size: 1.1rem;">{{ targetUser.email || '-' }}</p>
          </div>
          <div>
            <span class="form-label">{{$t('Privileges') }}</span>
            <div style="margin-top: 0.25rem;">
              <span v-if="targetUser.is_superuser" class="badge badge-high" style="margin-inline-end: 0.25rem;">
                {{ $t('Superuser') }}
              </span>
              <span v-if="targetUser.is_staff && !targetUser.is_superuser" class="badge badge-open" style="margin-inline-end: 0.25rem;">
                {{ $t('Support Staff') }}
              </span>
              <span v-if="!targetUser.is_staff && !targetUser.is_superuser" class="badge badge-resolved">
                {{ $t('Regular User') }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <h4 style="font-weight: 700; margin-bottom: 1.25rem;">
      📂 {{ $t('User Tickets History') }}
    </h4>

    <div v-if="ticketsLoading" style="text-align: center; padding: 2rem;">
      <p>{{ $t('Loading tickets...') }}</p>
    </div>

    <div class="card" v-else-if="userTickets.length > 0">
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>{{ $t('Ticket') }}</th>
              <th>{{ $t('Priority') }}</th>
              <th>{{ $t('Status') }}</th>
              <th>{{ $t('Category') }}</th>
              <th style="text-align: end;">{{ $t('Created At') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ticket in userTickets" :key="ticket.id" @click="$router.push(`/tickets/${ticket.id}`)">
              <td>
                <div style="font-weight: 600; color: var(--text-main);">{{ ticket.subject }}</div>
                <span class="text-muted" style="font-size: 0.8rem;">#{{ ticket.id }}</span>
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
                <span class="text-muted">
                  {{ $t(ticket.category) }}
                </span>
              </td>
              <td style="text-align: end; font-size: 0.85rem; color: var(--text-muted);">
                {{ formatDate(ticket.created_at) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card" v-else style="text-align: center; padding: 3rem;">
      <p class="text-muted">{{ $t('No tickets registered for this user.') }}</p>
    </div>
  </div>
</template>