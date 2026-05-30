<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { authState } from '../auth.js'
import { i18nState, t } from '../i18n.js'

const route = useRoute()
const router = useRouter()
const ticketId = route.params.id

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

const fetchTicketDetails = async () => {
  loading.value = true
  try {
    const response = await axios.get(`/api/tickets/${ticketId}/`)
    ticket.value = response.data
    newStatus.value = ticket.value.status
    await fetchReplies()
  } catch (err) {
    error.value = locale.value === 'ar' ? 'فشل تحميل تفاصيل التذكرة.' : 'Failed to load ticket details.'
  } finally {
    loading.value = false
  }
}

const fetchReplies = async () => {
  repliesLoading.value = true
  try {
    const response = await axios.get(`/api/replies/`, {
      params: { ticket: ticketId, page: repliesPage.value }
    })
    replies.value = response.data.results
    repliesCount.value = response.data.count
    repliesHasNext.value = response.data.has_next
    repliesHasPrev.value = response.data.has_previous
  } catch (err) {
    console.error('Failed to load replies', err)
  } finally {
    repliesLoading.value = false
  }
}

const handleAddReply = async () => {
  if (!replyText.value.trim()) return
  actionLoading.value = true
  error.value = ''
  message.value = ''
  try {
    await axios.post('/api/replies/', {
      ticket: ticketId,
      message: replyText.value
    })
    replyText.value = ''
    repliesPage.value = 1
    await fetchReplies()
    message.value = locale.value === 'ar' ? 'تم إضافة الرد بنجاح.' : 'Reply added successfully.'
  } catch (err) {
    error.value = err.response?.data?.detail || (locale.value === 'ar' ? 'فشل إضافة الرد.' : 'Failed to add reply.')
  } finally {
    actionLoading.value = false
  }
}

const handleUpdateStatus = async () => {
  actionLoading.value = true
  error.value = ''
  message.value = ''
  try {
    const response = await axios.put(`/api/tickets/${ticketId}/`, {
      status: newStatus.value
    })
    ticket.value = response.data
    message.value = locale.value === 'ar' ? 'تم تحديث حالة التذكرة.' : 'Ticket status updated.'
  } catch (err) {
    error.value = err.response?.data?.detail || (locale.value === 'ar' ? 'فشل تحديث الحالة.' : 'Failed to update status.')
  } finally {
    actionLoading.value = false
  }
}

const handleDeleteTicket = async () => {
  const confirmMsg = locale.value === 'ar' ? 'هل أنت متأكد من أرشفة هذه التذكرة؟' : 'Archive this ticket?'
  if (!confirm(confirmMsg)) return
  actionLoading.value = true
  error.value = ''
  try {
    await axios.delete(`/api/tickets/${ticketId}/`)
    router.push('/tickets')
  } catch (err) {
    error.value = err.response?.data?.detail || (locale.value === 'ar' ? 'فشل حذف التذكرة.' : 'Failed to delete ticket.')
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

onMounted(() => {
  fetchTicketDetails()
})
</script>

<template>
  <div v-if="loading" style="text-align: center; padding: 3rem;">
    <p>{{ locale === 'ar' ? 'جاري تحميل تفاصيل التذكرة...' : 'Loading ticket details...' }}</p>
  </div>

  <div v-else-if="error && !ticket" class="alert alert-danger">
    {{ error }}
  </div>

  <div v-else-if="ticket">
    <div style="margin-bottom: 1.5rem; display: flex; gap: 0.5rem; align-items: center; font-size: 0.9rem;">
      <router-link to="/tickets" style="font-weight: 500;">
        {{ locale === 'ar' ? 'التذاكر' : 'Tickets' }}
      </router-link>
      <span class="text-muted">/</span>
      <span class="text-muted">#{{ ticket.id }}</span>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; margin-bottom: 2rem;">
      <div>
        <h2 style="font-weight: 700; margin-bottom: 0.5rem;">{{ ticket.subject }}</h2>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.85rem; color: var(--text-muted);">
          <span>👤 {{ ticket.created_by_name }}</span>
          <span>📁 {{ 
            locale === 'ar' ? 
            (ticket.category === 'Technical' ? 'تقني' : ticket.category === 'Billing' ? 'فواتير' : 'عام') : 
            ticket.category 
          }}</span>
          <span>📅 {{ formatDate(ticket.created_at) }}</span>
        </div>
      </div>

      <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.5rem;">
        <span :class="['badge', `badge-${ticket.status === 'In Progress' ? 'progress' : ticket.status.toLowerCase()}`]" style="font-size: 0.95rem; padding: 0.4rem 1rem; border-radius: 20px;">
          {{ 
            locale === 'ar' ? 
            (ticket.status === 'Open' ? 'مفتوحة' : ticket.status === 'In Progress' ? 'قيد التنفيذ' : ticket.status === 'Resolved' ? 'تم حلها' : 'مغلقة') : 
            ticket.status 
          }}
        </span>
        <span :class="['badge', `badge-${ticket.priority.toLowerCase()}`]" style="font-size: 0.8rem; padding: 0.2rem 0.6rem;">
          {{ 
            locale === 'ar' ? 
            (ticket.priority === 'High' ? 'أولوية عالية' : ticket.priority === 'Medium' ? 'أولوية متوسطة' : 'أولوية منخفضة') : 
            `${ticket.priority} Priority`
          }}
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
            <span>{{ locale === 'ar' ? 'وصف المشكلة' : 'Issue Description' }}</span>
          </div>
          <div class="card-body">
            <div style="background-color: var(--bg-soft); padding: 1.5rem; border-radius: 12px; border-inline-start: 5px solid var(--accent-blue); font-size: 1.05rem; white-space: pre-wrap; margin-bottom: 1.5rem;">
              {{ ticket.description }}
            </div>

            <div v-if="ticket.attachment">
              <h6 class="form-label" style="margin-bottom: 0.5rem;">{{ locale === 'ar' ? 'المرفقات' : 'Attachment' }}</h6>
              <div style="display: inline-block; padding: 0.5rem; border: 1px solid var(--border-color); border-radius: 10px; background: var(--bg-soft);">
                <a :href="ticket.attachment" target="_blank">
                  <img :src="ticket.attachment" style="max-width: 250px; max-height: 250px; border-radius: 6px; display: block; object-fit: contain;" alt="Attachment" />
                </a>
              </div>
            </div>
          </div>
        </div>

        <h5 style="font-weight: 700; margin-bottom: 1.5rem;">
          💬 {{ locale === 'ar' ? 'سجل المحادثة' : 'Support Thread' }}
        </h5>

        <div class="thread-container" v-if="replies.length > 0">
          <div v-for="reply in replies" :key="reply.id" :class="['reply-bubble', reply.is_staff ? 'staff' : 'client']">
            <div class="reply-header">
              <span class="name">
                {{ reply.user_fullname || reply.user_name }}
                <span v-if="reply.is_staff" class="badge badge-open" style="font-size: 0.65rem; margin-inline-start: 0.25rem;">
                  {{ locale === 'ar' ? 'موظف' : 'STAFF' }}
                </span>
              </span>
              <span class="time">{{ formatDate(reply.created_at) }}</span>
            </div>
            <div class="reply-content">{{ reply.message }}</div>
          </div>

          <div class="pagination" v-if="repliesHasNext || repliesHasPrev">
            <button :disabled="!repliesHasPrev" @click="repliesPage--; fetchReplies();" class="page-btn">
              {{ locale === 'ar' ? 'السابق' : 'Prev' }}
            </button>
            <span class="page-info">{{ locale === 'ar' ? 'صفحة' : 'Page' }} {{ repliesPage }}</span>
            <button :disabled="!repliesHasNext" @click="repliesPage++; fetchReplies();" class="page-btn">
              {{ locale === 'ar' ? 'التالي' : 'Next' }}
            </button>
          </div>
        </div>

        <div class="card" v-else-if="!repliesLoading" style="text-align: center; padding: 3rem; margin-bottom: 2rem;">
          <span style="font-size: 2.5rem; display: block; opacity: 0.3; margin-bottom: 0.5rem;">💬</span>
          <p class="text-muted">{{ locale === 'ar' ? 'لا توجد رسائل في هذه المحادثة بعد.' : 'No messages in this thread yet.' }}</p>
        </div>

        <div v-if="ticket.status !== 'Closed'">
          <div class="card" v-if="isSupportStaff" style="margin-top: 2rem;">
            <div class="card-body">
              <h6 class="form-label">{{ locale === 'ar' ? 'كتابة رد' : 'Compose Reply' }}</h6>
              <form @submit.prevent="handleAddReply">
                <div class="form-group">
                  <textarea v-model="replyText" class="form-control" rows="4" :placeholder="locale === 'ar' ? 'اكتب ردك الاحترافي هنا...' : 'Your professional response...'" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary" :disabled="actionLoading || !replyText.trim()">
                  {{ locale === 'ar' ? 'إرسال الرد' : 'Send Response' }}
                </button>
              </form>
            </div>
          </div>

          <div class="alert alert-warning" v-else-if="user && user.is_superuser" style="margin-top: 2rem;">
            <span>ℹ️</span>
            <span>
              {{ locale === 'ar' ? 'بصفتك مديراً، أنت في وضع العرض فقط. الموظفون المختصون فقط هم من يمكنهم الرد.' : 'As a Manager, you are in View Only mode. Only assigned support staff can reply.' }}
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
          🔒 {{ locale === 'ar' ? 'هذه التذكرة مغلقة ومؤرشفة. لا يمكن اتخاذ أي إجراء آخر.' : 'This ticket is closed and archived. No further action is possible.' }}
        </div>
      </div>

      <div v-if="isAnyStaff">
        <div class="card" style="position: sticky; top: 90px;">
          <div class="card-header">
            <span>{{ locale === 'ar' ? 'إجراءات الإشراف' : 'Staff Actions' }}</span>
          </div>
          <div class="card-body">
            <div v-if="ticket.status !== 'Closed'" style="margin-bottom: 1.5rem;">
              <label class="form-label">{{ locale === 'ar' ? 'تحديث الحالة' : 'Update Status' }}</label>
              <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                <select v-model="newStatus" class="form-select">
                  <option value="Open">{{ locale === 'ar' ? 'مفتوحة' : 'Open' }}</option>
                  <option value="In Progress">{{ locale === 'ar' ? 'قيد التنفيذ' : 'In Progress' }}</option>
                  <option value="Resolved">{{ locale === 'ar' ? 'تم حلها' : 'Resolved' }}</option>
                  <option value="Closed">{{ locale === 'ar' ? 'مغلقة' : 'Closed' }}</option>
                </select>
                <button @click="handleUpdateStatus" class="btn btn-primary btn-sm" :disabled="actionLoading || newStatus === ticket.status">
                  {{ locale === 'ar' ? 'تحديث الحالة' : 'Update Status' }}
                </button>
              </div>
            </div>

            <div v-if="ticket.status === 'Closed'">
              <label class="form-label" style="color: var(--color-high);">{{ locale === 'ar' ? 'أرشفة السجل' : 'Archive Ticket' }}</label>
              <p class="text-muted" style="font-size: 0.8rem; margin-bottom: 0.75rem;">
                {{ locale === 'ar' ? 'التذاكر المغلقة فقط يمكن حذفها من النظام.' : 'Only closed tickets can be removed from the system.' }}
              </p>
              <button @click="handleDeleteTicket" class="btn btn-danger btn-sm" style="width: 100%;" :disabled="actionLoading">
                {{ locale === 'ar' ? 'حذف السجل' : 'Delete Record' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
