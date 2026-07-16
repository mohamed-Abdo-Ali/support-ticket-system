<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import Chart from 'chart.js/auto'
import { i18nState, t } from '../i18n.js'
import { useDashboardViewModel } from '../viewmodels/useDashboardViewModel.js'

const { stats, loading, error, user, fetchStats } = useDashboardViewModel()

const locale = computed(() => i18nState.locale)

let categoryChartInstance = null
let statusChartInstance = null

const getStats = async () => {
  await fetchStats(t)
  if (!error.value) {
    renderCharts()
  }
}

const renderCharts = () => {
  setTimeout(() => {
    if (categoryChartInstance) categoryChartInstance.destroy()
    if (statusChartInstance) statusChartInstance.destroy()

    const statusLabelsMapped = stats.value.status_labels.map(label => t(label))
    const categoryLabelsMapped = stats.value.category_labels.map(label => t(label))

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
            label: t('Ticket Count'),
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
              ticks: { color: textColor, stepSize: 1, },
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
  getStats()
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
      <p>{{ $t('Loading dashboard...') }}</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <div class="stat-grid">

        <router-link :to="{ path: '/tickets'  }" >
          <div class="stat-card stat-total">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
              <h6>{{ $t('Total Tickets') }}</h6>
              <h3>{{ stats.total_tickets }}</h3>
            </div>
          </div>
        </router-link>

        <router-link :to="{ path: '/tickets', query: { status: 'Open' } }" >
          <div class="stat-card stat-open">
            <div class="stat-icon">📩</div>
            <div class="stat-content">
              <h6>{{ $t('Open') }}</h6>
              <h3>{{ stats.open_tickets }}</h3>
            </div>
          </div>
        </router-link>

        <router-link :to="{ path: '/tickets', query: { status: 'Resolved' } }" >
          <div class="stat-card stat-resolved">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <h6>{{ $t('Resolved') }}</h6>
              <h3>{{ stats.resolved_tickets }}</h3>
            </div>
          </div>
        </router-link>


        <router-link :to="{ path: '/tickets', query: { status: 'closed' } }" >
        <div class="stat-card stat-critical">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <h6>{{ $t('closed') }}</h6>
            <h3>{{ stats.closed_tickets }}</h3>
          </div>
        </div>
        </router-link>

         <router-link :to="{ path: '/tickets', query: { status: 'In Progress' } }" >
        
        <div class="stat-card stat-critical">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <h6>{{ $t('In Progress') }}</h6>
            <h3>{{ stats.in_progress_tickets }}</h3>
          </div>
        </div>
        </router-link>

        
        <router-link :to="{ path: '/tickets', query: { priority: 'high' } }" >
          <div class="stat-card stat-critical">
            <div class="stat-icon">🔥</div>
            <div class="stat-content">
              <h6>{{ $t('Critical') }}</h6>
              <h3>{{ stats.high_priority_tickets }}</h3>
            </div>
          </div>
        </router-link>

        <router-link :to="{ path: '/tickets', query: { priority: 'Low' } }" >
          <div class="stat-card stat-critical">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
              <h6>{{ $t('Low') }}</h6>
              <h3>{{ stats.Low_priority_tickets }}</h3>
            </div>
          </div>
        </router-link>
        
        <router-link :to="{ path: '/tickets', query: { priority: 'Medium' } }" >
          <div class="stat-card stat-critical">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
              <h6>{{ $t('Medium') }}</h6>
              <h3>{{ stats.Medium_priority_tickets }}</h3>
            </div>
          </div>
        </router-link>
        
       

      </div>
 
      <div class="layout-columns">
        
        <div class="card">
          <div class="card-header">
            <span>{{ $t('System Activity Overview') }}</span>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas id="categoryChart"></canvas>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <span>{{ $t('Ticket Status') }}</span>
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
          <span>{{ $t('Browse Tickets') }}</span>
        </router-link>
        <router-link to="/tickets/new" class="btn btn-outline" v-if="user && !user.is_staff">
          <span>➕</span>
          <span>{{ $t('New Support Request') }}</span>
        </router-link>
      </div>

      
    </div>
  </div>
</template>
