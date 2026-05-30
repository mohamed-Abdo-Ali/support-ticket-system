<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'
import { authState } from '../auth.js'
import { i18nState, t } from '../i18n.js'

const stats = ref({
  total_tickets: 0,
  open_tickets: 0,
  resolved_tickets: 0,
  high_priority_tickets: 0,
  category_labels: [],
  category_counts: [],
  status_labels: [],
  status_counts: []
})
const loading = ref(true)
const error = ref('')

const locale = computed(() => i18nState.locale)
const user = computed(() => authState.user)

let categoryChartInstance = null
let statusChartInstance = null

const fetchStats = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/dashboard/')
    stats.value = response.data
    renderCharts()
  } catch (err) {
    error.value = locale.value === 'ar' ? 'فشل تحميل بيانات لوحة التحكم.' : 'Failed to load dashboard data.'
  } finally {
    loading.value = false
  }
}

const renderCharts = () => {
  setTimeout(() => {
    if (categoryChartInstance) categoryChartInstance.destroy()
    if (statusChartInstance) statusChartInstance.destroy()

    const isAr = locale.value === 'ar'

    const statusLabelsMapped = stats.value.status_labels.map(label => {
      if (isAr) {
        if (label === 'Open') return 'مفتوحة'
        if (label === 'In Progress') return 'قيد التنفيذ'
        if (label === 'Resolved') return 'تم حلها'
        if (label === 'Closed') return 'مغلقة'
      }
      return label
    })

    const categoryLabelsMapped = stats.value.category_labels.map(label => {
      if (isAr) {
        if (label === 'Technical') return 'تقني'
        if (label === 'Billing') return 'فواتير'
        if (label === 'General') return 'عام'
      }
      return label
    })

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
    const textColor = isDark ? '#94a3b8' : '#64748b'
    const gridColor = isDark ? '#1e293b' : '#f1f5f9'

    const statusCtx = document.getElementById('statusChart')
    if (statusCtx) {
      statusChartInstance = new Chart(statusCtx, {
        type: 'doughnut',
        data: {
          labels: statusLabelsMapped,
          datasets: [{
            data: stats.value.status_counts,
            backgroundColor: ['#3b82f6', '#0d9488', '#10b981', '#ef4444'],
            hoverOffset: 12,
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                usePointStyle: true,
                padding: 20,
                color: textColor
              }
            }
          },
          cutout: '70%'
        }
      })
    }

    const categoryCtx = document.getElementById('categoryChart')
    if (categoryCtx) {
      categoryChartInstance = new Chart(categoryCtx, {
        type: 'bar',
        data: {
          labels: categoryLabelsMapped,
          datasets: [{
            label: isAr ? 'عدد التذاكر' : 'Tickets Received',
            data: stats.value.category_counts,
            backgroundColor: '#3b82f6',
            borderRadius: 8,
            maxBarThickness: 45
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: gridColor },
              ticks: { color: textColor }
            },
            x: {
              grid: { display: false },
              ticks: { color: textColor }
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      })
    }
  }, 100)
}

onMounted(() => {
  fetchStats()
})

onUnmounted(() => {
  if (categoryChartInstance) categoryChartInstance.destroy()
  if (statusChartInstance) statusChartInstance.destroy()
})

watch(locale, () => {
  if (!loading.value) {
    renderCharts()
  }
})
</script>

<template>
  <div>
    <div v-if="loading" style="text-align: center; padding: 3rem;">
      <p>{{ locale === 'ar' ? 'جاري تحميل لوحة التحكم...' : 'Loading dashboard...' }}</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <div class="stat-grid">
        <div class="stat-card stat-total">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <h6>{{ locale === 'ar' ? 'إجمالي التذاكر' : 'Total Tickets' }}</h6>
            <h3>{{ stats.total_tickets }}</h3>
          </div>
        </div>

        <div class="stat-card stat-open">
          <div class="stat-icon">📩</div>
          <div class="stat-content">
            <h6>{{ locale === 'ar' ? 'مفتوحة' : 'Open' }}</h6>
            <h3>{{ stats.open_tickets }}</h3>
          </div>
        </div>

        <div class="stat-card stat-resolved">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <h6>{{ locale === 'ar' ? 'تم حلها' : 'Resolved' }}</h6>
            <h3>{{ stats.resolved_tickets }}</h3>
          </div>
        </div>

        <div class="stat-card stat-critical">
          <div class="stat-icon">🔥</div>
          <div class="stat-content">
            <h6>{{ locale === 'ar' ? 'عالية الأهمية' : 'Critical' }}</h6>
            <h3>{{ stats.high_priority_tickets }}</h3>
          </div>
        </div>
      </div>

      <div class="layout-columns">
        <div class="card">
          <div class="card-header">
            <span>{{ locale === 'ar' ? 'نظرة عامة على النشاط' : 'System Activity Overview' }}</span>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas id="categoryChart"></canvas>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <span>{{ locale === 'ar' ? 'حالة التذاكر' : 'Ticket Status' }}</span>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas id="statusChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <div style="display: flex; justify-content: center; gap: 1.5rem; margin-top: 3rem; margin-bottom: 2rem;">
        <router-link to="/tickets" class="btn btn-primary">
          <span>📋</span>
          <span>{{ locale === 'ar' ? 'استعراض التذاكر' : 'Browse Tickets' }}</span>
        </router-link>
        <router-link to="/tickets/new" class="btn btn-outline" v-if="user && !user.is_staff">
          <span>➕</span>
          <span>{{ locale === 'ar' ? 'طلب دعم جديد' : 'New Support Request' }}</span>
        </router-link>
      </div>
    </div>
  </div>
</template>
