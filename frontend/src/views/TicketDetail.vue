<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { t } from '../i18n.js'
import { useTicketDetailViewModel } from '../viewmodels/useTicketDetailViewModel.js'

const route = useRoute()
const router = useRouter()
const ticketId = route.params.id

const {
  ticket,
  replies,
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
} = useTicketDetailViewModel()

const getReplies = () => {
  fetchReplies(ticketId)
}

const addReply = () => {
  handleAddReply(ticketId, t)
}

const updateStatus = () => {
  handleUpdateStatus(ticketId, t)
}

const deleteTicket = () => {
  handleDeleteTicket(ticketId, t, () => {
    router.push('/tickets')
  })
}

onMounted(() => {
  fetchTicketDetails(ticketId, t)
})
</script>

<template>
  <div v-if="loading" style="text-align: center; padding: 3rem;">
    <p>{{ $t('Loading ticket details...') }}</p>
  </div>

  <div v-else-if="error && !ticket" class="alert alert-danger">
    {{ error }}
  </div>

  <div v-else-if="ticket">
    <div style="margin-bottom: 1.5rem; display: flex; gap: 0.5rem; align-items: center; font-size: 0.9rem;">
      <router-link to="/tickets" style="font-weight: 500;">
        {{ $t('Tickets') }}
      </router-link>
      <span class="text-muted">/</span>
      <span class="text-muted">#{{ ticket.id }}</span>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; margin-bottom: 2rem;">
      <div>
        <h2 style="font-weight: 700; margin-bottom: 0.5rem;">{{ ticket.subject }}</h2>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.85rem; color: var(--text-muted);">
          <span>👤 {{ ticket.created_by_name }}</span>
          <span>📁 {{ $t(ticket.category) }}</span>
          <span>📅 {{ formatDate(ticket.created_at) }}</span>
        </div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.5rem;">
        <span :class="['badge', `badge-${ticket.status === 'In Progress' ? 'progress' : ticket.status.toLowerCase()}`]" style="font-size: 0.95rem; padding: 0.4rem 1rem; border-radius: 20px;">
          {{ $t(ticket.status) }}
        </span>
        <span :class="['badge', `badge-${ticket.priority.toLowerCase()}`]" style="font-size: 0.8rem; padding: 0.2rem 0.6rem;">
          {{ $t(ticket.priority) }}
        </span>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger" style="margin-bottom: 1.5rem;">
      <span>⚠️</span>
      <span>{{ t(error) || error }}</span>
    </div>
    <div v-if="message" class="alert alert-success" style="margin-bottom: 1.5rem;">
      <span>✅</span>
      <span>{{ t(message) || message }}</span>
    </div>

    <div class="layout-columns">
      <div>
        <div class="card" style="margin-bottom: 2rem;">
          <div class="card-header">
            <span>{{ $t('Issue Description') }}</span>
          </div>
          <div class="card-body">
            <div style="background-color: var(--bg-soft); padding: 1.5rem; border-radius: 12px; border-inline-start: 5px solid var(--accent-blue); font-size: 1.05rem; white-space: pre-wrap; margin-bottom: 1.5rem;">
              {{ ticket.description }}
            </div>

            <div v-if="ticket.attachment">
              <h6 class="form-label" style="margin-bottom: 0.5rem;">{{ $t('Attachment') }}</h6>
              <div style="display: inline-block; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: 10px; background: var(--bg-soft);">
                <a :href="ticket.attachment" target="_blank">
                  <img :src="ticket.attachment" style="max-width: 250px; max-height: 250px; border-radius: 6px; display: block; object-fit: contain;" alt="Attachment" />
                </a>
              </div>
            </div>
          </div>
        </div>

        <h5 style="font-weight: 700; margin-bottom: 1.5rem;">
          💬 {{ $t('Support Thread') }}
        </h5>

        <div class="thread-container" v-if="replies.length > 0">
          <div v-for="reply in replies" :key="reply.id" :class="['reply-bubble', reply.is_staff ? 'staff' : 'client']">
            <div class="reply-header">
              <span class="name">
                {{ reply.user_fullname || reply.user_name }}
                <span v-if="reply.is_staff" class="badge badge-open" style="font-size: 0.65rem; margin-inline-start: 0.25rem;">
                  {{ $t('STAFF') }}
                </span>
              </span>
              <span class="time">{{ formatDate(reply.created_at) }}</span>
            </div>
            <div class="reply-content">{{ reply.message }}</div>
          </div>

          <div class="pagination" v-if="repliesHasNext || repliesHasPrev">
            <button :disabled="!repliesHasPrev" @click="repliesPage--; getReplies();" class="page-btn">
              {{ $t('Prev') }}
            </button>
            <span class="page-info">{{ $t('Page') }} {{ repliesPage }}</span>
            <button :disabled="!repliesHasNext" @click="repliesPage++; getReplies();" class="page-btn">
              {{ $t('Next') }}
            </button>
          </div>
        </div>

        <div class="card" v-else-if="!repliesLoading" style="text-align: center; padding: 3rem; margin-bottom: 2rem;">
          <span style="font-size: 2.5rem; display: block; opacity: 0.3; margin-bottom: 0.5rem;">💬</span>
          <p class="text-muted">{{ $t('No messages in this thread yet.') }}</p>
        </div>

        <div v-if="ticket.status !== 'Closed'">
          <div class="card" v-if="isSupportStaff" style="margin-top: 2rem;">
            <div class="card-body">
              <h6 class="form-label">{{ $t('Compose Reply') }}</h6>
              <form @submit.prevent="addReply">
                <div class="form-group">
                  <textarea v-model="replyText" class="form-control" rows="4" :placeholder="$t('Your professional response...')" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary" :disabled="actionLoading || !replyText.trim()">
                  {{ $t('Send Response') }}
                </button>
              </form>
            </div>
          </div>

          <div class="alert alert-warning" v-else-if="user && user.is_superuser" style="margin-top: 2rem;">
            <span>ℹ️</span>
            <span>
              {{ $t('As a Manager, you are in View Only mode. Only assigned support staff can reply.') }}
            </span>
          </div>

          <div class="alert alert-info" v-else style="margin-top: 2rem;">
            <span>ℹ️</span>
            <span>
              {{ locale === 'ar' ? 'مهندسو الدعم لدينا يراجعون تذكرتك حالياً. سيتم إخطارك بأي تحديثات.' : 'Our support engineers are reviewing your ticket. You\'ll be notified of any updates.' }}
            </span>
          </div>
        </div>

        <div class="alert alert-danger" v-else style="text-align: center; margin-top: 2rem; display: block;">
          🔒 {{ $t('This ticket is closed and archived. No further action is possible.') }}
        </div>
      </div>

      <div v-if="isAnyStaff">
        <div class="card" style="position: sticky; top: 90px;">
          <div class="card-header">
            <span>{{ $t('Staff Actions') }}</span>
          </div>
          <div class="card-body">
            <div v-if="ticket.status !== 'Closed'" style="margin-bottom: 1.5rem;">
              <label class="form-label">{{ $t('Update Status') }}</label>
              <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                <select v-model="newStatus" class="form-select">
                  <option value="Open">{{ $t('Open') }}</option>
                  <option value="In Progress">{{ $t('In Progress') }}</option>
                  <option value="Resolved">{{ $t('Resolved') }}</option>
                  <option value="Closed">{{ $t('Closed') }}</option>
                </select>
                <button @click="updateStatus" class="btn btn-primary btn-sm" :disabled="actionLoading || newStatus === ticket.status">
                  {{ $t('Update Status') }}
                </button>
              </div>
            </div>

            <div v-if="ticket.status === 'Closed'">
              <label class="form-label" style="color: var(--color-high);">{{ $t('Archive Ticket') }}</label>
              <p class="text-muted" style="font-size: 0.8rem; margin-bottom: 0.75rem;">
                {{ $t('Only closed tickets can be removed from the system.') }}
              </p>
              <button @click="deleteTicket" class="btn btn-danger btn-sm" style="width: 100%;" :disabled="actionLoading">
                {{ $t('Delete Record') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
