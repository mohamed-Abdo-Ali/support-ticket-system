<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { i18nState, t } from '../i18n.js'

const route = useRoute()
const userId = route.params.id

const targetUser = ref(null)
const userTickets = ref([])
const loading = ref(true)
const ticketsLoading = ref(true)
const error = ref('')

const locale = computed(() => i18nState.locale)

const fetchUserDetails = async () => {
  loading.value = true
  try {
    const response = await axios.get(`/api/users/${userId}/`)
    targetUser.value = response.data
    await fetchUserTickets()
  } catch (err) {
    error.value = locale.value === 'ar' ? 'فشل تحميل بيانات المستخدم.' : 'Failed to load user details.'
  } finally {
    loading.value = false
  }
}

const fetchUserTickets = async () => {
  ticketsLoading.value = true
  try {
    const response = await axios.get('/api/tickets/', {
      params: { created_by: userId }
    })
    userTickets.value = response.data.results
  } catch (err) {
    console.error('Failed to load user tickets', err)
  } finally {
    ticketsLoading.value = false
  }
}

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
  fetchUserDetails()
})
</script>

<template>
  <div v-if="loading" style="text-align: center; padding: 3rem;">
    <p>{{ locale === 'ar' ? 'جاري تحميل تفاصيل المستخدم...' : 'Loading user details...' }}</p>
  </div>

  <div v-else-if="error" class="alert alert-danger">
    {{ error }}
  </div>

  <div v-else-if="targetUser">
    <div style="margin-bottom: 1.5rem; display: flex; gap: 0.5rem; align-items: center; font-size: 0.9rem;">
      <router-link to="/users" style="font-weight: 500;">
        {{ locale === 'ar' ? 'إدارة المستخدمين' : 'User Management' }}
      </router-link>
      <span class="text-muted">/</span>
      <span class="text-muted">{{ targetUser.username }}</span>
    </div>

    <div class="card" style="margin-bottom: 2rem;">
      <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
        <span>{{ locale === 'ar' ? 'بيانات الحساب' : 'User Account Info' }}</span>
        <router-link :to="`/users/${targetUser.id}/edit`" class="btn btn-primary btn-sm">
          <span>✏️</span>
          <span>{{ locale === 'ar' ? 'تعديل البيانات' : 'Edit' }}</span>
        </router-link>
      </div>
      <div class="card-body">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
          <div>
            <span class="form-label">{{ locale === 'ar' ? 'اسم المستخدم' : 'Username' }}</span>
            <p style="font-size: 1.1rem; font-weight: 600;">{{ targetUser.username }}</p>
          </div>
          <div>
            <span class="form-label">{{ locale === 'ar' ? 'الاسم الكامل' : 'Full Name' }}</span>
            <p style="font-size: 1.1rem;">{{ targetUser.fullname || '-' }}</p>
          </div>
          <div>
            <span class="form-label">{{ locale === 'ar' ? 'البريد الإلكتروني' : 'Email Address' }}</span>
            <p style="font-size: 1.1rem;">{{ targetUser.email || '-' }}</p>
          </div>
          <div>
            <span class="form-label">{{ locale === 'ar' ? 'الصلاحيات' : 'Privileges' }}</span>
            <div style="margin-top: 0.25rem;">
              <span v-if="targetUser.is_superuser" class="badge badge-high" style="margin-inline-end: 0.25rem;">
                {{ locale === 'ar' ? 'مدير نظام' : 'Superuser' }}
              </span>
              <span v-if="targetUser.is_staff && !targetUser.is_superuser" class="badge badge-open" style="margin-inline-end: 0.25rem;">
                {{ locale === 'ar' ? 'موظف دعم' : 'Support Staff' }}
              </span>
              <span v-if="!targetUser.is_staff && !targetUser.is_superuser" class="badge badge-resolved">
                {{ locale === 'ar' ? 'مستخدم عادي' : 'Regular User' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <h4 style="font-weight: 700; margin-bottom: 1.25rem;">
      📂 {{ locale === 'ar' ? 'التذاكر الخاصة بالمستخدم' : 'User Tickets History' }}
    </h4>

    <div v-if="ticketsLoading" style="text-align: center; padding: 2rem;">
      <p>{{ locale === 'ar' ? 'جاري تحميل التذاكر...' : 'Loading tickets...' }}</p>
    </div>

    <div class="card" v-else-if="userTickets.length > 0">
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>{{ locale === 'ar' ? 'التذكرة' : 'Ticket' }}</th>
              <th>{{ locale === 'ar' ? 'الأولوية' : 'Priority' }}</th>
              <th>{{ locale === 'ar' ? 'الحالة' : 'Status' }}</th>
              <th>{{ locale === 'ar' ? 'التصنيف' : 'Category' }}</th>
              <th style="text-align: end;">{{ locale === 'ar' ? 'تاريخ الإنشاء' : 'Created At' }}</th>
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
                <span class="text-muted">
                  {{ 
                    locale === 'ar' ? 
                    (ticket.category === 'Technical' ? 'تقني' : ticket.category === 'Billing' ? 'فواتير' : 'عام') : 
                    ticket.category 
                  }}
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
      <p class="text-muted">{{ locale === 'ar' ? 'لا توجد تذاكر مسجلة لهذا المستخدم.' : 'No tickets registered for this user.' }}</p>
    </div>
  </div>
</template>
