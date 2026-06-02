<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { i18nState, t } from '../i18n.js'

const users = ref([])
const loading = ref(true)
const error = ref('')

const locale = computed(() => i18nState.locale)

const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/users/')
    users.value = response.data
  } catch (err) {
    error.value = t('Failed to load user list.')
  } finally {
    loading.value = false
  }
}

const handleDeleteUser = async (id, username) => {
  // استخدام دالة الترجمة مع دمج المتغير بشكل مرن وقابل للترجمة الديناميكية
  const confirmMsg = t('Are you sure you want to delete user {username}?').replace('{username}', username)
  if (!confirm(confirmMsg)) return
  try {
    await axios.delete(`/api/users/${id}/`)
    users.value = users.value.filter(u => u.id !== id)
  } catch (err) {
    alert(err.response?.data?.detail || t('Failed to delete user.'))
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
  fetchUsers()
})
</script>

<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem;">
      <div>
        <h2 style="font-weight: 700; margin-bottom: 0.25rem;">
          {{ $t('User Management') }}
        </h2>
        <p class="text-muted" style="margin-bottom: 0;">
          {{ $t('Manage system accounts and assign privileges') }}
        </p>
      </div>
      <router-link to="/users/new" class="btn btn-primary">
        <span>➕</span>
        <span>{{ $t('Add User') }}</span>
      </router-link>
    </div>

    <div v-if="loading" style="text-align: center; padding: 3rem;">
      <p>{{ $t('Loading user list...') }}</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div class="card" v-else-if="users.length > 0">
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>{{ $t('Username') }}</th>
              <th>{{ $t('Full Name') }}</th>
              <th>{{ $t('Email Address') }}</th>
              <th>{{ $t('Role / Permissions') }}</th>
              <th>{{ $t('Ticket Count') }}</th>
              <th>{{ $t('Joined Date') }}</th>
              <th style="text-align: end;">{{ $t('Actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id" @click="$router.push(`/users/${u.id}`)">
              <td>
                <span style="font-weight: 600; color: var(--text-main);">{{ u.username }}</span>
              </td>
              <td>{{ u.fullname || '-' }}</td>
              <td>{{ u.email || '-' }}</td>
              <td>
                <div style="display: flex; gap: 0.25rem; flex-wrap: wrap;">
                  <span v-if="u.is_superuser" class="badge badge-high" style="font-size: 0.7rem;">
                    {{ $t('Manager / Admin') }}
                  </span>
                  <span v-if="u.is_staff && !u.is_superuser" class="badge badge-open" style="font-size: 0.7rem;">
                    {{ $t('Support Staff') }}
                  </span>
                  <span v-if="!u.is_staff && !u.is_superuser" class="badge badge-resolved" style="font-size: 0.7rem;">
                    {{ $t('Regular User') }}
                  </span>
                </div>
              </td>
              <td>
                <span class="badge badge-closed">{{ u.ticket_count }}</span>
              </td>
              <td style="font-size: 0.85rem; color: var(--text-muted);">
                {{ formatDate(u.date_joined) }}
              </td>
              <td style="text-align: end;" @click.stop>
                <div style="display: flex; gap: 0.5rem; justify-content: flex-end;">
                  <router-link :to="`/users/${u.id}/edit`" class="btn btn-outline btn-sm" style="padding: 0.25rem 0.5rem;">
                    ✏️
                  </router-link>
                  <button @click="handleDeleteUser(u.id, u.username)" class="btn btn-danger btn-sm" style="padding: 0.25rem 0.5rem;">
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card" v-else style="text-align: center; padding: 4rem 2rem;">
      <p class="text-muted">{{ $t('No users found in the system.') }}</p>
    </div>
  </div>
</template>