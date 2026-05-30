<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { authState } from '../auth.js'
import { i18nState, t } from '../i18n.js'

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

const fetchTickets = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      q: search.value,
      status: selectedStatus.value,
      priority: selectedPriority.value
    }
    const response = await axios.get('/api/tickets/', { params })
    tickets.value = response.data.results
    count.value = response.data.count
  } catch (err) {
    error.value = locale.value === 'ar' ? 'فشل تحميل التذاكر.' : 'Failed to load tickets.'
  } finally {
    loading.value = false
  }
}

const applyFilters = () => {
  page.value = 1
  fetchTickets()
}

const resetFilters = () => {
  search.value = ''
  selectedStatus.value = ''
  selectedPriority.value = ''
  page.value = 1
  fetchTickets()
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

onMounted(() => {
  fetchTickets()
})

watch(page, () => {
  fetchTickets()
})
</script>

<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem;">
      <div>
        <h2 style="font-weight: 700; margin-bottom: 0.25rem;">
          {{ locale === 'ar' ? 'مستودع التذاكر' : 'Ticket Repository' }}
        </h2>
        <p class="text-muted" style="margin-bottom: 0;">
          {{ locale === 'ar' ? 'استعرض وإدارة جميع طلبات الدعم' : 'Browse and manage all support interactions' }}
        </p>
      </div>
      <router-link to="/tickets/new" class="btn btn-primary" v-if="user && !user.is_staff">
        <span>➕</span>
        <span>{{ locale === 'ar' ? 'تذكرة جديدة' : 'New Ticket' }}</span>
      </router-link>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <div class="card-body">
        <form @submit.prevent="applyFilters" class="filters-grid">
          <div class="form-group" style="margin-bottom: 0;">
            <label class="form-label">{{ locale === 'ar' ? 'بحث سريع' : 'Quick Search' }}</label>
            <input type="text" v-model="search" class="form-control" :placeholder="locale === 'ar' ? 'الموضوع أو كلمة مفتاحية...' : 'Subject or Keyword...'" />
          </div>

          <div class="form-group" style="margin-bottom: 0;">
            <label class="form-label">{{ locale === 'ar' ? 'الحالة' : 'Status' }}</label>
            <select v-model="selectedStatus" class="form-select">
              <option value="">{{ locale === 'ar' ? 'جميع الحالات' : 'All Statuses' }}</option>
              <option value="Open">{{ locale === 'ar' ? 'مفتوحة' : 'Open' }}</option>
              <option value="In Progress">{{ locale === 'ar' ? 'قيد التنفيذ' : 'In Progress' }}</option>
              <option value="Resolved">{{ locale === 'ar' ? 'تم حلها' : 'Resolved' }}</option>
              <option value="Closed">{{ locale === 'ar' ? 'مغلقة' : 'Closed' }}</option>
            </select>
          </div>

          <div class="form-group" style="margin-bottom: 0;">
            <label class="form-label">{{ locale === 'ar' ? 'الأولوية' : 'Priority' }}</label>
            <select v-model="selectedPriority" class="form-select">
              <option value="">{{ locale === 'ar' ? 'جميع الأولويات' : 'All Priorities' }}</option>
              <option value="Low">{{ locale === 'ar' ? 'منخفضة' : 'Low' }}</option>
              <option value="Medium">{{ locale === 'ar' ? 'متوسطة' : 'Medium' }}</option>
              <option value="High">{{ locale === 'ar' ? 'عالية' : 'High' }}</option>
            </select>
          </div>

          <div style="display: flex; gap: 0.5rem; justify-content: flex-end;">
            <button type="submit" class="btn btn-primary" style="flex: 1;">
              {{ locale === 'ar' ? 'تصفية' : 'Filter' }}
            </button>
            <button type="button" @click="resetFilters" class="btn btn-outline" style="flex: 1;">
              {{ locale === 'ar' ? 'إعادة تعيين' : 'Reset' }}
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
              <th>{{ locale === 'ar' ? 'التذكرة' : 'Ticket' }}</th>
              <th>{{ locale === 'ar' ? 'الأولوية' : 'Priority' }}</th>
              <th>{{ locale === 'ar' ? 'الحالة' : 'Status' }}</th>
              <th>{{ locale === 'ar' ? 'التصنيف' : 'Category' }}</th>
              <th>{{ locale === 'ar' ? 'المالك' : 'Owner' }}</th>
              <th style="text-align: end;">{{ locale === 'ar' ? 'تاريخ الإنشاء' : 'Created At' }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ticket in tickets" :key="ticket.id" @click="$router.push(`/tickets/${ticket.id}`)">
              <td>
                <div style="font-weight: 600; color: var(--text-main);">{{ ticket.subject }}</div>
                <div class="text-muted" style="font-size: 0.8rem;">#{{ ticket.id }}</div>
                <span v-if="ticket.is_late" class="badge badge-late" style="margin-top: 0.25rem;">
                  {{ locale === 'ar' ? 'متأخرة' : 'Overdue' }}
                </span>
              </td>
              <td>
                <span :class="['badge', `badge-${ticket.priority.toLowerCase()}`]">
                  {{ 
                    locale === 'ar' ? 
                    (ticket.priority === 'High' ? 'عالية' : ticket.priority === 'Medium' ? 'متوسطة' : 'منخفضة') : 
                    ticket.priority 
                  }}
                </span>
              </td>
              <td>
                <span :class="['badge', `badge-${ticket.status === 'In Progress' ? 'progress' : ticket.status.toLowerCase()}`]">
                  {{ 
                    locale === 'ar' ? 
                    (ticket.status === 'Open' ? 'مفتوحة' : ticket.status === 'In Progress' ? 'قيد التنفيذ' : ticket.status === 'Resolved' ? 'تم حلها' : 'مغلقة') : 
                    ticket.status 
                  }}
                </span>
              </td>
              <td>
                <span class="text-muted" style="font-size: 0.9rem;">
                  {{ 
                    locale === 'ar' ? 
                    (ticket.category === 'Technical' ? 'تقني' : ticket.category === 'Billing' ? 'فواتير' : 'عام') : 
                    ticket.category 
                  }}
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
      <h4 style="margin-bottom: 0.5rem;">{{ locale === 'ar' ? 'لا توجد تذاكر' : 'No tickets found' }}</h4>
      <p class="text-muted">{{ locale === 'ar' ? 'لا توجد تذاكر تطابق معايير البحث.' : 'No tickets match your selection.' }}</p>
    </div>

    <div v-else-if="loading" style="text-align: center; padding: 4rem 2rem;">
      <p>{{ locale === 'ar' ? 'جاري تحميل التذاكر...' : 'Loading tickets...' }}</p>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button :disabled="page === 1" @click="page--" class="page-btn">
        {{ locale === 'ar' ? 'السابق' : 'Prev' }}
      </button>
      <span class="page-info">
        {{ locale === 'ar' ? 'صفحة' : 'Page' }} {{ page }} / {{ totalPages }}
      </span>
      <button :disabled="page === totalPages" @click="page++" class="page-btn">
        {{ locale === 'ar' ? 'التالي' : 'Next' }}
      </button>
    </div>
  </div>
</template>
